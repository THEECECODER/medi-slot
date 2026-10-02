from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.diagnostic_centre import DiagnosticCentre
from app.models.diagnostic_test import DiagnosticTest
from app.models.centre_test import CentreTest
from app.schemas.centre import CentreCreate, CentreResponse
from app.schemas.test import TestCreate, TestResponse
from app.api.deps import get_current_user

router = APIRouter(
    tags=["Centres & Tests"]
)


@router.post(
    "/centres",
    response_model=CentreResponse,
    status_code=status.HTTP_201_CREATED
)
def create_centre(
    data: CentreCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    centre = DiagnosticCentre(
        name=data.name,
        location=data.location
    )

    db.add(centre)
    db.commit()
    db.refresh(centre)

    return centre


@router.get("/centres", response_model=list[CentreResponse])
def list_centres(db: Session = Depends(get_db)):
    return db.query(DiagnosticCentre).all()


@router.post(
    "/tests",
    response_model=TestResponse,
    status_code=status.HTTP_201_CREATED
)
def create_test(
    data: TestCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    test = DiagnosticTest(
        name=data.name,
        description=data.description
    )

    db.add(test)
    db.commit()
    db.refresh(test)

    return test


@router.get("/tests", response_model=list[TestResponse])
def list_tests(db: Session = Depends(get_db)):
    return db.query(DiagnosticTest).all()


@router.post("/centres/{centre_id}/tests/{test_id}")
def add_test_to_centre(
    centre_id: int,
    test_id: int,
    price: float,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    centre = db.query(DiagnosticCentre).filter(
        DiagnosticCentre.id == centre_id
    ).first()

    test = db.query(DiagnosticTest).filter(
        DiagnosticTest.id == test_id
    ).first()

    if not centre or not test:
        raise HTTPException(
            status_code=404,
            detail="Centre or test not found"
        )

    existing = db.query(CentreTest).filter(
        CentreTest.centre_id == centre_id,
        CentreTest.test_id == test_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Test already available at this centre"
        )

    centre_test = CentreTest(
        centre_id=centre_id,
        test_id=test_id,
        price=price
    )

    db.add(centre_test)
    db.commit()

    return {
        "message": "Test added to centre",
        "centre_id": centre_id,
        "test_id": test_id,
        "price": price
    }