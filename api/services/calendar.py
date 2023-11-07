from datetime import datetime

from bson import ObjectId
from fastapi import HTTPException
from api.schemas.appointment import Appointment, AppointmentCreation, BusinessHours, DayAppointments
from api.utils.responses import json_encoder
from config.mongoCon import MongoCon
from pymongo.command_cursor import CommandCursor


def set_businness_hours(doctor_id: str, business_hours: BusinessHours) -> bool:
    with MongoCon() as cnx:
        result = cnx.users.update_one({"_id": ObjectId(doctor_id), "role": "doctor"}, {
                                      "$set": {"business_hours": business_hours.model_dump()}})
    return result.matched_count > 0

# TODO: Return BusinessHours model
def get_business_hours(doctor_id: str) -> BusinessHours:
    with MongoCon() as cnx:
        result = cnx.users.find_one({"_id": ObjectId(doctor_id)}, {
                                    "_id": 0, "business_hours": 1})
    if not result:
        return None
    return result["business_hours"]

# TODO: Return Appointment model
def create_appointment(appointment: AppointmentCreation) -> Appointment:
    if (appointment.end_datetime < appointment.start_datetime):
        raise HTTPException(
            status_code=400, detail="The appointment end time must be greater than the start time")
    business_hours = BusinessHours(**get_business_hours(appointment.doctor_id))
    if business_hours:
        in_business_hours = verify_business_hours_for_appointment(appointment, business_hours)
        if not in_business_hours:
            raise HTTPException(
                status_code=400, detail="The appointment is not within the doctor's business hours")
    if not check_appointment_disponibility(appointment):
        raise HTTPException(
            status_code=400, detail="The appointment is not available because the doctor already has an appointment at that time")
    with MongoCon() as cnx:
        new_appointment = appointment.model_dump()
        new_appointment["doctor_id"] = ObjectId(appointment.doctor_id)
        new_appointment["patient_id"] = ObjectId(appointment.patient_id)
        insert_result = cnx.appointments.insert_one(new_appointment)
    created_appointment = get_appointments(
        {"_id": insert_result.inserted_id}).next()
    return created_appointment


def check_appointment_disponibility(appointment: AppointmentCreation) -> bool:
    with MongoCon() as cnx:
        result = cnx.appointments.find_one(
            {
                "doctor_id": ObjectId(appointment.doctor_id),
                "$or": [
                    {
                        "start_datetime": {
                            "$gte": appointment.start_datetime,
                            "$lt": appointment.end_datetime
                        }
                    },
                    {
                        "end_datetime": {
                            "$gt": appointment.start_datetime,
                            "$lte": appointment.end_datetime
                        }
                    }
                ]
            }
        )
    if result:
        return False
    return True


def verify_business_hours_for_appointment(appointment: AppointmentCreation, business_hours: BusinessHours) -> bool:
    appointment_start_time = appointment.start_datetime.time()
    appointment_end_time = appointment.end_datetime.time()
    business_hours_start_time = datetime.strptime(
        business_hours.start_time, "%H:%M").time()
    business_hours_end_time = datetime.strptime(
        business_hours.end_time, "%H:%M").time()
    if appointment_start_time < business_hours_start_time or appointment_end_time > business_hours_end_time:
        return False
    return True


def get_appointments(match_stage: dict) -> CommandCursor:
    with MongoCon() as cnx:
        result = cnx.appointments.aggregate([
            {"$match": match_stage},
            {"$lookup": {
                "from": "patients",
                "localField": "patient_id",
                "foreignField": "_id",
                "as": "patient"
            }},
            {"$unwind": "$patient"},
            {"$sort": {"start_datetime": 1}},
            {"$project": {
                "_id": 1,
                "patient": {"_id": 1, "name": 1, "lastname": 1, "email": 1},
                "cause": 1,
                "start_datetime": 1,
                "end_datetime": 1,
                "status": 1
            }}
        ])
    return result

# TODO: Return DayAppointments model
def get_day_appointments(doctor_id: str, date: str) -> DayAppointments:
    date = datetime.strptime(date, "%Y-%m-%d")
    business_hours = get_business_hours(doctor_id)
    result = get_appointments({
        "doctor_id": ObjectId(doctor_id),
        "start_datetime": {
            "$gte": date,
            "$lt": date.replace(hour=23, minute=59)
        }
    })
    appointments = list(result)
    return {'business_hours': business_hours, 'appointments': appointments}
