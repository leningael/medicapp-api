from typing import List
from fastapi import APIRouter, Body
from api.schemas.receptionist import Receptionist
import api.services.receptionist as receptionist_service
from api.utils.responses import json_encoder, success_ok, not_found


receptionist_router = APIRouter(tags=["receptionist"], prefix="/receptionist")

@receptionist_router.get('/all_receptionists', response_model=List[Receptionist])
def get_all_receptionists(doctor_id: str = None, search: str = None):
    receptionists = receptionist_service.get_all_receptionists(doctor_id, search)
    return json_encoder(receptionists)

@receptionist_router.get('/dr_receptionists/{doctor_id}', response_model=List[Receptionist])
def get_receptionists(doctor_id: str, search: str = None):
    receptionists = receptionist_service.get_dr_receptionists(doctor_id, search)
    return json_encoder(receptionists)

@receptionist_router.put('/assign_doctor')
def assign_doctor(receptionist_id: str = Body(), doctor_id: str = Body()):
    result = receptionist_service.assign_doctor(receptionist_id, doctor_id)
    if not result:
        return not_found("Receptionist")
    return success_ok()

@receptionist_router.put('/unassign_doctor')
def unassign_doctor(receptionist_id: str = Body(), doctor_id: str = Body()):
    result = receptionist_service.unassign_doctor(receptionist_id, doctor_id)
    if not result:
        return not_found("Receptionist")
    return success_ok()