from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.catalog import router as catalog_router
from app.api.bookings import router as booking_router
from app.api.payments import router as payment_router

app = FastAPI(
    title="MediSlot API",
    description="Healthcare Diagnostic Booking Platform",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(catalog_router)
app.include_router(booking_router)
app.include_router(payment_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}