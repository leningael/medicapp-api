from pydantic import BaseModel
from typing import Optional

class Notes(BaseModel):
    ...

class NoteOverview(BaseModel):
    _id: str
    patientName: str
    reason: str
    startDate: str
    endDate: str

class NoteContent(BaseModel):
    _id: str
    reason: Optional[str]
    diagnosis: str
    temperature: str
    weight: str
    height: str
    imc: int
    systolicPressure: str
    diastolicPressure: str