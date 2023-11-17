import datetime

from pydantic import BaseModel, Field
from typing import List, Union
from api.schemas.patient import PatientOverview

class NoteOverview(BaseModel):
    id: Union[str, None] = Field(default=None,alias='_id')
    patient: Union[PatientOverview,None] = None
    reason: Union[str,None] = None
    date: Union[datetime.datetime, None] = None

class Medicament(BaseModel):
    id: Union[str, None] = Field(default=None,alias='_id')
    medicament: str
    quantity: str
    consume_method: str
    frequency: str
    duration: str
    notes: str

class NoteContent(BaseModel):
    id: Union[str,None] = Field(default=None,alias='_id')
    reason: Union[str,None] = None
    diagnosis: str
    temperature: str
    weight: str
    height: str
    imc: float
    sistolic_pressure: str
    diastolic_pressure: str
    medication: Union[List[Medicament], None] = None
    notes: Union[str, None] = None
    
class Note(BaseModel):
    id: Union[str, None] = Field(default=None,alias='_id')
    appointment_id: Union[str, None] = None
    patient: PatientOverview 
    doctor_name: str
    date: Union[datetime.datetime, None]  = Field(default=datetime.datetime.now())
    content: NoteContent
