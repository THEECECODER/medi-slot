from pydantic import BaseModel


class CentreCreate(BaseModel):
    name: str
    location: str


class CentreResponse(BaseModel):
    id: int
    name: str
    location: str

    class Config:
        from_attributes = True