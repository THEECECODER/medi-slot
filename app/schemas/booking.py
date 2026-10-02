from datetime import datetime
from pydantic import BaseModel


class BookingCreate(BaseModel):
    centre_id: int
    test_id: int
    appointment_at: datetime


class BookingResponse(BaseModel):
    id: int
    centre_id: int
    test_id: int
    appointment_at: datetime
    amount: float
    status: str

    class Config:
        from_attributes = True