from bson import ObjectId
from api.schemas.patient import Patient
from config.mongoCon import MongoCon


class patientService():

    def get_patients(self):
        with MongoCon() as cnx:
            patients_list = cnx.patients.find()
            if not patients_list:
                return None
            print(patients_list)
            return list(patients_list)
        
    def get_patient(self, id: str) :
        with MongoCon() as cnx:
            patient = cnx.patients.find_one({"_id": ObjectId(id)})
            patient['_id'] = str(patient['_id'])
            if not patient:
                return None
            return patient
        
    def add_patient(self, patient: Patient):
        with MongoCon() as cnx:
            new_patient = patient.model_dump()
            response = cnx.patients.insert_one(new_patient)
            print(response)
            if not response:
                return None
            return response
        
    def update_patient(self, id: str, patient: Patient):
        with MongoCon() as cnx:
            response = cnx.patients.find_one_and_update({"_id": ObjectId(id)}, {"$set": patient.dict()})
            if not response:
                return None
            return response  
        
    def delete_patient(self, id: str):
        with MongoCon() as cnx:
            response = cnx.patients.find_one_and_delete({"_id": ObjectId(id)})
            if not response:
                return None
            return response