from fastapi import APIRouter, HTTPException

from api.schemas.appointment import Appointment, AppointmentCreation, BusinessHours, DayAppointments
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