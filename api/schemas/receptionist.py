from pydantic import BaseModel, Field


class Receptionist(BaseModel):
    id: str = Field(alias="_id")
    name: str
    lastname: str
    email: str