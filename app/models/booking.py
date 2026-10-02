from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric, String
from sqlalchemy.sql import func

from app.db.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    centre_id = Column(
        Integer,
        ForeignKey("diagnostic_centres.id"),
        nullable=False
    )

    test_id = Column(
        Integer,
        ForeignKey("diagnostic_tests.id"),
        nullable=False
    )

    appointment_at = Column(DateTime(timezone=True), nullable=False)

    amount = Column(Numeric(10, 2), nullable=False)

    status = Column(
        String(20),
        nullable=False,
        default="PENDING"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )