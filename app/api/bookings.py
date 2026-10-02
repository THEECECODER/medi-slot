from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user
from app.models.booking import Booking
from app.models.centre_test import CentreTest
from app.schemas.booking import BookingCreate, BookingResponse

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.post(
    "/",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED
)
def create_booking(
    data: BookingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    centre_test = db.query(CentreTest).filter(
        CentreTest.centre_id == data.centre_id,
        CentreTest.test_id == data.test_id
    ).first()

    if not centre_test:
        raise HTTPException(
            status_code=404,
            detail="Test is not available at this centre"
        )

    booking = Booking(
        user_id=current_user.id,
        centre_id=data.centre_id,
        test_id=data.test_id,
        appointment_at=data.appointment_at,
        amount=centre_test.price,
        status="PENDING"
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking


@router.get("/", response_model=list[BookingResponse])
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return db.query(Booking).filter(
        Booking.user_id == current_user.id
    ).all()


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    return booking


@router.patch("/{booking_id}/cancel")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if booking.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail="Only pending bookings can be cancelled"
        )

    booking.status = "CANCELLED"
    db.commit()

    return {
        "message": "Booking cancelled",
        "booking_id": booking.id
    }