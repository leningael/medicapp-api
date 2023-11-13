from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

class BusinessHours(BaseModel):
    start_time: str
    end_time: str

class AppointmentCreation(BaseModel):
    doctor_id: str
    patient_id: str
    cause: str
    start_datetime: datetime
    end_datetime: datetime

class PatientInfo(BaseModel):
    id: str = Field(alias="_id")
    name: str
    lastname: str
    email: str

class Appointment(BaseModel):
    id: str = Field(alias="_id")
    cause: str
    start_datetime: datetime
    end_datetime: datetime
    patient: PatientInfo

class PatientAppointment(BaseModel):
    id: str = Field(alias="_id")
    cause: str
    start_datetime: datetime
    end_datetime: datetime
    status: str

class DayAppointments(BaseModel):
    business_hours: BusinessHours
    appointments: List[Appointment]

class AppointmentMove(BaseModel):
    appointment_id: str
    start_datetime: datetime
    end_datetime: datetime