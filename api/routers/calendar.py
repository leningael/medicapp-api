from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from api.schemas.appointment import Appointment, AppointmentCreation, AppointmentMove, BusinessHours, DayAppointments, PatientAppointment
import api.services.calendar as calendar_service
from api.utils.responses import json_encoder, success_ok, not_found


calendar_router = APIRouter(tags=["calendar"], prefix="/calendar")

@calendar_router.put("/set_businness_hours/{doctor_id}")
def set_businness_hours(doctor_id: str, business_hours: BusinessHours):
    result = calendar_service.set_businness_hours(doctor_id, business_hours)
    if not result:
        not_found("Doctor")
    return success_ok()

@calendar_router.post("/create_appointment", response_model=Appointment)
def create_appointment(appointment: AppointmentCreation):
    try:
        result = calendar_service.create_appointment(appointment)
        return JSONResponse(content=json_encoder(result), status_code=201)
    except HTTPException as e:
        return JSONResponse(content={"error": str(e.detail)}, status_code=e.status_code)

@calendar_router.get("/get_day_appointments/{doctor_id}", response_model=DayAppointments)
def get_day_appointments(doctor_id: str, date: str):
    appointments = calendar_service.get_day_appointments(doctor_id, date)
    return json_encoder(appointments)

@calendar_router.get("/get_patient_appointments/{doctor_id}/{patient_id}", response_model=List[PatientAppointment])
def get_patient_appointments(doctor_id: str, patient_id: str):
    appointments = calendar_service.get_patient_appointments(doctor_id, patient_id)
    if not appointments:
        return not_found("Appointments")
    return json_encoder(appointments)

@calendar_router.get("/get_active_appointments/{doctor_id}", response_model=List[Appointment])
def get_active_appointments(doctor_id: str):
    appointments = calendar_service.get_active_appointments(doctor_id)
    if not appointments:
        raise HTTPException(status_code=404, detail="Appointments not found")
    return json_encoder(appointments)

@calendar_router.delete("/delete_appointment/{appointment_id}")
def delete_appointment(appointment_id: str):
    result = calendar_service.delete_appointment(appointment_id)
    if not result:
        return not_found("Appointment")
    return success_ok()

@calendar_router.put("/move_appointment")
def move_appointment(move_data: AppointmentMove):
    result = calendar_service.move_appointment(move_data)
    if not result:
        return not_found("Appointment")
    return success_ok()