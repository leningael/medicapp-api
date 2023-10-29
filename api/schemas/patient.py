from typing import List
from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    lastname: str
    gender: str
    curp: str
    birthdate: str
    phone: str
    email: str
    address: str
    zipcode: str
    bloodtype: str
    owner: List[str]

    