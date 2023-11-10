from typing import List
from fastapi import APIRouter, HTTPException

from api.schemas.appointment import Appointment, AppointmentCreation, AppointmentMove, BusinessHours, DayAppointments, PatientAppointment
import api.services.calendar as calendar_service
from api.utils.responses import json_encoder, success_ok, not_found


calendar_router = APIRouter(tags=["calendar"], prefix="/calendar")

@calendar_router.put("/set_businness_hours/{doctor_id}")
def set_businness_hours(doctor_id: str, business_hours: BusinessHours):
    result = calendar_service.set_businness_hours(doctor_id, business_hours)
    if not result:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return success_ok()

@calendar_router.post("/create_appointment", response_model=Appointment)
def create_appointment(appointment: AppointmentCreation):
    result = calendar_service.create_appointment(appointment)
    return json_encoder(result)

@calendar_router.get("/get_day_appointments/{doctor_id}", response_model=DayAppointments)
def get_day_appointments(doctor_id: str, date: str):
    appointments = calendar_service.get_day_appointments(doctor_id, date)
    return json_encoder(appointments)

@calendar_router.get("/get_patient_appointments/{doctor_id}/{patient_id}", response_model=List[PatientAppointment])
def get_patient_appointments(doctor_id: str, patient_id: str):
    appointments = calendar_service.get_patient_appointments(doctor_id, patient_id)
    if not appointments:
        raise HTTPException(status_code=404, detail="Appointments not found")
    return json_encoder(appointments)

@calendar_router.delete("/delete_appointment/{appointment_id}")
def delete_appointment(appointment_id: str):
    result = calendar_service.delete_appointment(appointment_id)
    if not result:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return success_ok()

@calendar_router.put("/move_appointment")
def move_appointment(move_data: AppointmentMove):
    result = calendar_service.move_appointment(move_data)
    if not result:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return success_ok()