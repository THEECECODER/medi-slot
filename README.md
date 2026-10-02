# MediSlot

MediSlot is a backend API for booking diagnostic tests at healthcare diagnostic centres.

The system provides authentication, diagnostic centre and test management, appointment booking, simulated payments, and idempotent payment webhook processing.

## Tech Stack

- Python 3.13+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT Authentication
- bcrypt
- Pydantic
- Docker & Docker Compose
- Pytest
- Swagger / OpenAPI

## Features

- User signup and login
- JWT-based authentication
- Diagnostic centre management
- Diagnostic test management
- Centre-test mapping with pricing
- Appointment booking
- Booking ownership protection
- Simulated payment processing
- Payment success/failure handling
- Idempotent payment webhook
- PostgreSQL database
- Alembic database migrations
- Dockerized API and PostgreSQL
- Automated API tests
- Swagger/OpenAPI documentation

---

# How to Run

## Prerequisites

Make sure you have the following installed:

- Python 3.13+
- Docker Desktop
- Git

## Option 1: Run Everything with Docker

### 1. Clone the repository

```bash
git clone https://github.com/THEECECODER/medi-slot.git
cd medi-slot
```

### 2. Build and start the API and PostgreSQL

```bash
docker compose up --build -d
```

### 3. Run database migrations

```bash
docker compose exec api alembic upgrade head
```

### 4. Verify the containers

```bash
docker compose ps
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger/OpenAPI documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

### Stop the application

```bash
docker compose down
```

---

## Option 2: Run the API Locally

### 1. Start PostgreSQL using Docker

```bash
docker compose up -d postgres
```

### 2. Create a Python virtual environment

#### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

#### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the `.env` file

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://medislot:medislot@localhost:5432/medislot
JWT_SECRET=change-this-later
JWT_ALGORITHM=HS256
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the API

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Authentication

### Signup

```http
POST /auth/signup
```

Request:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

Response:

```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
```

### Login

```http
POST /auth/login
```

Request:

```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

Response:

```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
```

### Current User

```http
GET /auth/me
```

Requires:

```text
Authorization: Bearer <JWT_TOKEN>
```

Response:

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```

---

# Diagnostic Centres

### Create Centre

```http
POST /centres
```

Authentication required.

Request:

```json
{
  "name": "Apollo Diagnostics",
  "location": "New Delhi"
}
```

Response:

```json
{
  "id": 1,
  "name": "Apollo Diagnostics",
  "location": "New Delhi"
}
```

### List Centres

```http
GET /centres
```

Response:

```json
[
  {
    "id": 1,
    "name": "Apollo Diagnostics",
    "location": "New Delhi"
  }
]
```

---

# Diagnostic Tests

### Create Test

```http
POST /tests
```

Authentication required.

Request:

```json
{
  "name": "Complete Blood Count",
  "description": "Basic blood examination"
}
```

### List Tests

```http
GET /tests
```

Response:

```json
[
  {
    "id": 1,
    "name": "Complete Blood Count",
    "description": "Basic blood examination"
  }
]
```

---

# Centre-Test Mapping

A diagnostic test can be available at multiple centres, with each centre having its own price.

### Add Test to Centre

```http
POST /centres/{centre_id}/tests/{test_id}?price=500
```

Example:

```http
POST /centres/1/tests/1?price=500
```

Response:

```json
{
  "message": "Test added to centre",
  "centre_id": 1,
  "test_id": 1,
  "price": 500
}
```

The database uses a composite primary key:

```text
centre_id + test_id
```

This prevents duplicate centre-test mappings.

---

# Bookings

### Create Booking

```http
POST /bookings/
```

Authentication required.

Request:

```json
{
  "centre_id": 1,
  "test_id": 1,
  "appointment_at": "2026-10-05T10:30:00"
}
```

The price is calculated by the server from the centre-test mapping.

Response:

```json
{
  "id": 1,
  "centre_id": 1,
  "test_id": 1,
  "appointment_at": "2026-10-05T10:30:00",
  "amount": 500,
  "status": "PENDING"
}
```

### Get My Bookings

```http
GET /bookings/
```

Returns bookings belonging to the authenticated user.

### Get Booking

```http
GET /bookings/{booking_id}
```

Users cannot access another user's booking.

### Cancel Booking

```http
PATCH /bookings/{booking_id}/cancel
```

Only `PENDING` bookings can be cancelled.

The booking status changes to:

```text
CANCELLED
```

---

# Payments

Payments are simulated for this project.

### Create Payment

```http
POST /payments/
```

Authentication required.

Request:

```json
{
  "booking_id": 1,
  "success": true
}
```

If payment succeeds:

```text
Payment: SUCCESS
Booking: CONFIRMED
```

If payment fails:

```text
Payment: FAILED
Booking: FAILED
```

Example response:

```json
{
  "id": 1,
  "booking_id": 1,
  "provider_event_id": "sim_xxxxxxxx",
  "amount": 500,
  "status": "SUCCESS"
}
```

---

# Payment Webhook

```http
POST /payments/webhook/
```

Example request:

```json
{
  "provider_event_id": "evt_12345",
  "booking_id": 1,
  "amount": 500,
  "status": "SUCCESS"
}
```

The webhook updates the payment and booking status.

## Webhook Idempotency

Every webhook contains a unique:

```text
provider_event_id
```

This field has a unique database constraint.

If the same webhook is received again, the existing payment is returned instead of creating a duplicate payment.

Example:

```json
{
  "message": "Webhook already processed",
  "payment_id": 1
}
```

---

# Database / Schema Design

The application uses PostgreSQL with SQLAlchemy and Alembic.

## Users

Stores registered users.

```text
users
----------------
id
name
email
password_hash
created_at
```

`email` is unique and passwords are stored as bcrypt hashes.

## Diagnostic Centres

```text
diagnostic_centres
------------------
id
name
location
created_at
```

## Diagnostic Tests

```text
diagnostic_tests
----------------
id
name
description
created_at
```

## Centre Tests

Represents which tests are available at which centres.

```text
centre_tests
----------------
centre_id
test_id
price
```

The combination of `centre_id` and `test_id` is the composite primary key.

This allows the same test to have different prices at different centres.

## Bookings

```text
bookings
----------------
id
user_id
centre_id
test_id
appointment_at
amount
status
created_at
```

The booking stores the price at the time of booking.

Possible statuses:

```text
PENDING
CONFIRMED
FAILED
CANCELLED
```

## Payments

```text
payments
----------------
id
booking_id
provider_event_id
amount
status
created_at
```

`provider_event_id` is unique to support webhook idempotency.

---

# Booking and Payment Flow

```text
User
  |
  v
Signup / Login
  |
  v
JWT Authentication
  |
  v
Select Centre + Test
  |
  v
Create Booking
  |
  v
PENDING
  |
  v
Payment
  |
  +---- SUCCESS ----> CONFIRMED
  |
  +---- FAILED -----> FAILED
  |
  v
Payment Webhook
  |
  v
Idempotent Processing
```

---

# Important Assumptions

### Payment Provider

The payment system is simulated because no real payment gateway integration was provided.

### Webhook Security

The webhook currently assumes trusted requests.

A production implementation should verify payment-provider webhook signatures.

### Centre and Test Management

Centre and test creation requires authentication, but there is no separate admin role.

A production system would use role-based access control.

### Appointment Availability

The current implementation validates that a test is available at a centre but does not implement complete slot capacity or double-booking prevention.

### Price Handling

The booking amount is calculated server-side.

The client cannot directly set the booking price.

### Authentication

JWT access tokens expire after 60 minutes.

### Webhook Idempotency

`provider_event_id` is treated as the unique identifier for a payment event.

Repeated events with the same ID are treated as already processed.

---

# Edge Cases Handled

The API handles:

- Duplicate user registration
- Invalid login credentials
- Missing or invalid JWT
- Non-existent centres
- Non-existent tests
- Tests unavailable at a centre
- Duplicate centre-test mappings
- Invalid booking IDs
- Unauthorized access to another user's booking
- Cancelling non-pending bookings
- Paying for non-pending bookings
- Payment amount mismatch
- Failed payments
- Repeated payment webhooks

---

# Testing

The project uses Pytest.

Run the tests with:

```bash
pytest
```

Current automated tests cover:

- Health endpoint
- Protected endpoint without authentication
- Invalid login

Expected result:

```text
3 passed
```

---

# API Documentation

FastAPI automatically generates Swagger/OpenAPI documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# What I Would Improve With More Time

- Add role-based access control for administrators.
- Add appointment slot availability and double-booking prevention.
- Integrate a real payment provider.
- Verify webhook signatures.
- Add more comprehensive integration tests.
- Add pagination to listing endpoints.
- Add Redis-based rate limiting.
- Add Celery for asynchronous tasks.
- Add structured logging and monitoring.
- Improve transaction handling for concurrent payment/webhook requests.

---

# Project Structure

```text
medi-slot/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   └── main.py
├── alembic/
├── tests/
├── .env
├── .gitignore
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# License

This project was developed as a backend engineering assignment and portfolio project.