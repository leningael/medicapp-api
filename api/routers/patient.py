import json
from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse
from api.schemas.patient import Patient

from api.services.patient import patientService
from api.utils.responses import json_encoder


patient_router = APIRouter()

@patient_router.get("/patients")
def get_patients():
    patients= patientService().get_patients()
    if not patients:
        return JSONResponse({"message": "No patients found"}, status_code=status.HTTP_404_NOT_FOUND)
    return json_encoder(patients)

@patient_router.get("/patients/{id}")
def get_patient(id: str):
    patient = patientService().get_patient(id)
    if not patient:
        return JSONResponse({"message": "No patient found"}, status_code=status.HTTP_404_NOT_FOUND)
    return json_encoder(patient)

@patient_router.post("/patients")
def add_patient(patient: Patient):
    response = patientService().add_patient(patient)
    if not response:
        return JSONResponse({"message": "Patient could not be added"}, status_code=status.HTTP_409_CONFLICT)
    return JSONResponse({"message": "Patient added successfully"}, status_code=status.HTTP_201_CREATED)

@patient_router.put("/patients/{id}")
def update_patient(id: str, patient: Patient):
    response = patientService().update_patient(id, patient)
    if not response:
        return JSONResponse({"message": "Patient could not be updated"}, status_code=status.HTTP_409_CONFLICT)
    return JSONResponse({"message": "Patient updated successfully"}, status_code=status.HTTP_200_OK)

@patient_router.delete("/patients/{id}")
def delete_patient(id: str):
    response = patientService().delete_patient(id)
    if not response:
        return JSONResponse({"message": "Patient could not be deleted"}, status_code=status.HTTP_409_CONFLICT)
    return JSONResponse({"message": "Patient deleted successfully"}, status_code=status.HTTP_200_OK)