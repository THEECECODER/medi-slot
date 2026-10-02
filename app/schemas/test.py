from pydantic import BaseModel


class TestCreate(BaseModel):
    name: str
    description: str | None = None


class TestResponse(BaseModel):
    id: int
    name: str
    description: str | None

    class Config:
        from_attributes = True