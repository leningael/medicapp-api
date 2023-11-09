from bson import ObjectId
from api.schemas.patient import Patient, PatientOverview
from config.mongoCon import MongoCon
from pymongo import ReturnDocument


class PatientService():

    def get_all_existing_patients(self, search: str = None):
        with MongoCon() as cnx:
            find_condition = {}
            if search:
                find_condition = {"curp": {"$regex": search, "$options": "i"}}
            patients_list = cnx.patients.find(
                find_condition, {"_id": 1, "name": 1, "lastname": 1, "curp": 1})
            if not patients_list:
                return None
            return list(patients_list)

    def get_dr_patients(self, id: str, search: str = None):
        with MongoCon() as cnx:
            find_condition = {"doctors": ObjectId(id)}
            if search:
                search_fields = {
                    "$or":
                    [
                        {"name": {"$regex": search, "$options": "i"}},
                        {"lastname": {
                            "$regex": search, "$options": "i"}},
                        {"curp": {"$regex": search, "$options": "i"}}
                    ]
                }
                find_condition.update(search_fields)       
            patients_list = cnx.patients.find(find_condition, { "_id": 1, "name": 1, "lastname": 1, "curp": 1 })
            if not patients_list:
                return None
            return list(patients_list)

    def get_patient(self, id: str):
        with MongoCon() as cnx:
            patient = cnx.patients.find_one({"_id": ObjectId(id)})
            if not patient:
                return None
            return Patient(**patient)

    def add_patient(self, patient: Patient):
        with MongoCon() as cnx:
            new_patient = patient.model_dump()
            response = cnx.patients.insert_one(new_patient)
            if not response:
                return None
            return response

    def update_patient(self, id: str, patient: Patient):
        with MongoCon() as cnx:
            response = cnx.patients.find_one_and_update({"_id": ObjectId(
                id)}, {"$set": patient.dict()}, return_document=ReturnDocument.AFTER)
            if not response:
                return None
            return Patient(**response)

    def delete_patient(self, id: str):
        with MongoCon() as cnx:
            response = cnx.patients.find_one_and_delete({"_id": ObjectId(id)})
            if not response:
                return None
            return response
