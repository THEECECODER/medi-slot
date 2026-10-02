from pydantic import BaseModel


class PaymentCreate(BaseModel):
    booking_id: int
    success: bool = True


class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    provider_event_id: str
    amount: float
    status: str

    class Config:
        from_attributes = True


class PaymentWebhook(BaseModel):
    provider_event_id: str
    booking_id: int
    amount: float
    status: str