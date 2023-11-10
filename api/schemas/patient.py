from typing import List, Optional
from pydantic import BaseModel, Field

class ClinicalHistory(BaseModel):
    pathological: Optional[str]
    non_pathological: Optional[str]
    inherit: Optional[str]
    surgical: Optional[str]
    current_medication: Optional[str]
    allergies: Optional[str]
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
    doctors: List[str]
    clinical_history: Optional[ClinicalHistory] = None

class PatientOverview(BaseModel):
    id: str = Field(alias="_id")
    name: str
    lastname: str
    curp: str


    