from fastapi import APIRouter,status, Depends, HTTPException, Path
from typing import Annotated
from config.mongoCon import MongoCon

from api.services.user import get_curret_user
from bson.objectid import ObjectId


router = APIRouter(prefix="/patient",tags=["patient"])  
user_dependency = Annotated[dict, Depends(get_curret_user)]

@router.get("/",status_code=status.HTTP_200_OK)
async def read_patients(user : user_dependency):
    patients_arr = []
    with MongoCon() as cnx:
        patients = cnx.patients.find({"doctors":ObjectId(user.get("user_id"))},
                                     {"name":1,"lastname":1,"gender":1})
        for patient in patients:
            patient["_id"] =  str(patient.pop("_id"))  
            patients_arr.append(patient)
    return patients_arr    

@router.get("/{patient_id}")
async def read_patient_details(user: user_dependency, patient_id:str = Path(min_length=24,max_length=24)):
    with MongoCon() as cnx:
        patient = cnx.patients.find_one({"_id":ObjectId(patient_id),"doctors":ObjectId(user.get("user_id"))},
                                        {"doctors":0})
        if not patient:
            raise HTTPException(status_code=404,detail="Patient not found")
        patient["_id"] =  str(patient.pop("_id"))  
    return patient
    
