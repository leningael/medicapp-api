from typing import List
from fastapi import APIRouter
from api.schemas.doctor import DoctorOverview
import api.services.doctor as doctor_service
from api.utils.responses import json_encoder

doctor_router = APIRouter(tags=["doctors"])

@doctor_router.get('/get_receptionist_doctors/{receptionist_id}', response_model=List[DoctorOverview])
def get_receptionist_doctors(receptionist_id: str, search: str = None):
    doctors = doctor_service.get_receptionist_doctors(receptionist_id, search)
    return json_encoder(doctors)