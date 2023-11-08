from bson import ObjectId
from api.schemas.patient import Patient, PatientOverview
from api.utils.responses import json_encoder
from config.mongoCon import MongoCon
from pymongo import ReturnDocument 


class PatientService():

    def get_all_existing_patients(self, doctor_id: str = None, search: str = None):
        with MongoCon() as cnx:
            if (search):
               patients_list = cnx.patients.find(
                   {"doctors": {"$ne": ObjectId(doctor_id)}},
                   {"curp": {"$regex": search, '$options': 'i'}},
                   { "_id": 1, "name": 1, "lastname": 1, "curp": 1 }
                )
            if (doctor_id and not search):
                patients_list = cnx.patients.find(
                    {"doctors": {"$ne": ObjectId(doctor_id)}},
                    { "_id": 1, "name": 1, "lastname": 1, "curp": 1 }
                )
            else:
                patients_list = cnx.patients.find({},{ "_id": 1, "name": 1, "lastname": 1, "curp": 1 })
            if not patients_list:
                return None              
            return list(patients_list)
        
    def get_dr_patients(self, id: str, search: str = None):
        with MongoCon() as cnx:
            if search:
                patients_list = cnx.patients.find(
                {"doctors": ObjectId(id),
                "$or": [
                    { "name": { "$regex": search, '$options': 'i' } },
                    { "lastame": { "$regex": search },'$options': 'i'},
                    { "curp": { "$regex": search }, '$options': 'i'}
                ]}, { "_id": 1, "name": 1, "lastname": 1, "curp": 1 })
            else:
                patients_list = cnx.patients.find({"doctors": ObjectId(id)}, { "_id": 1, "name": 1, "lastname": 1, "curp": 1 })
            if not patients_list:
                return None      
            return list(patients_list) 
        
    def get_patient(self, id: str) :
        with MongoCon() as cnx:
            patient = cnx.patients.find_one({"_id": ObjectId(id)})
            if not patient:
                return None
            return patient
        
    def add_patient(self, patient: Patient):
        with MongoCon() as cnx:
            patient.doctors = [ObjectId(id) for id in patient.doctors]
            new_patient = patient.model_dump()
            response = cnx.patients.insert_one(new_patient)
            if not response:
                return None
            return response
        
    def add_doctor_to_patient(self, id_patient: str, id_doctor: str):
        with MongoCon() as cnx:
            response = cnx.patients.find_one_and_update({"_id": ObjectId(id_patient)}, {"$push": {"doctors": ObjectId(id_doctor)}}, return_document = ReturnDocument.AFTER)
            if not response:
                return None
            return response
        
    def update_patient(self, id: str, patient: Patient):
        with MongoCon() as cnx:
            response = cnx.patients.find_one_and_update({"_id": ObjectId(id)}, {"$set": patient.model_dump()}, return_document = ReturnDocument.AFTER)
            if not response:
                return None
            return response
        
    def delete_patient(self, id: str):
        with MongoCon() as cnx:
            response = cnx.patients.find_one_and_delete({"_id": ObjectId(id)})
            if not response:
                return None
            return response