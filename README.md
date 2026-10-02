# MediSlot

MediSlot is a backend API for diagnostic test discovery, appointment booking,
and simulated payment processing.

Built with FastAPI, PostgreSQL, SQLAlchemy, Alembic and JWT authentication.

## Features

- User signup and login
- JWT-based authentication
- Diagnostic centre management
- Diagnostic test management
- Centre/test pricing
- Authenticated appointment booking
- Booking ownership protection
- Simulated payments
- Payment success/failure handling
- Idempotent payment webhooks
- PostgreSQL persistence
- Alembic database migrations
- Automated API tests
- Swagger/OpenAPI documentation

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT
- bcrypt
- Pytest
- Docker

## Project Structure

```text
medi-slot/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   └── schemas/
├── alembic/
├── tests/
├── .env
├── docker-compose.yml
├── requirements.txt
└── README.md