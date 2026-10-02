import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.booking import Booking
from app.models.payment import Payment
from app.schemas.payment import (
    PaymentCreate,
    PaymentResponse,
    PaymentWebhook,
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post(
    "/",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_payment(
    data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    booking = db.query(Booking).filter(
        Booking.id == data.booking_id,
        Booking.user_id == current_user.id,
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    if booking.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail="Booking is not pending",
        )

    payment_status = "SUCCESS" if data.success else "FAILED"

    payment = Payment(
        booking_id=booking.id,
        provider_event_id=f"sim_{uuid.uuid4()}",
        amount=booking.amount,
        status=payment_status,
    )

    booking.status = (
        "CONFIRMED" if data.success else "FAILED"
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment


@router.post("/webhook/")
def payment_webhook(
    data: PaymentWebhook,
    db: Session = Depends(get_db),
):
    existing_payment = db.query(Payment).filter(
        Payment.provider_event_id == data.provider_event_id
    ).first()

    # Idempotency
    if existing_payment:
        return {
            "message": "Webhook already processed",
            "payment_id": existing_payment.id,
        }

    booking = db.query(Booking).filter(
        Booking.id == data.booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    if data.amount != float(booking.amount):
        raise HTTPException(
            status_code=400,
            detail="Payment amount mismatch",
        )

    payment = Payment(
        booking_id=booking.id,
        provider_event_id=data.provider_event_id,
        amount=data.amount,
        status=data.status,
    )

    if data.status == "SUCCESS":
        booking.status = "CONFIRMED"
    elif data.status == "FAILED":
        booking.status = "FAILED"

    db.add(payment)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()

        existing_payment = db.query(Payment).filter(
            Payment.provider_event_id == data.provider_event_id
        ).first()

        return {
            "message": "Webhook already processed",
            "payment_id": existing_payment.id if existing_payment else None,
        }

    db.refresh(payment)

    return {
        "message": "Webhook processed",
        "payment_id": payment.id,
    }