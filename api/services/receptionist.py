from typing import List
from bson import ObjectId
from api.schemas.receptionist import Receptionist
from config.mongoCon import MongoCon


def get_all_receptionists(doctor_id: str = None, search: str = None) -> List[Receptionist]:
    find_condition = {"role": "receptionist"}
    if doctor_id:
        find_condition.update({"doctors": {"$ne": ObjectId(doctor_id)}})
    if search:
        find_condition.update({
            "$or": [
                {"name": {"$regex": search, "$options": "i"}},
                {"lastname": {"$regex": search, "$options": "i"}}
            ]
        })
    with MongoCon() as cnx:
        receptionists = list(cnx.users.find(find_condition, {"password": 0}))
    return receptionists


def get_dr_receptionists(doctor_id: str, search: str = None) -> List[Receptionist]:
    find_condition = {"role": "receptionist", "doctors": ObjectId(doctor_id)}
    if search:
        find_condition.update({
            "$or": [
                {"name": {"$regex": search, "$options": "i"}},
                {"lastname": {"$regex": search, "$options": "i"}}
            ]
        })
    with MongoCon() as cnx:
        receptionists = list(cnx.users.find(find_condition, {"password": 0}))
    return receptionists


def assign_doctor(receptionist_id: str, doctor_id: str) -> bool:
    with MongoCon() as cnx:
        result = cnx.users.update_one(
            {"_id": ObjectId(receptionist_id)},
            {
                "$push": {"doctors": ObjectId(doctor_id)}
            })
    return result.matched_count > 0


def unassign_doctor(receptionist_id: str, doctor_id: str) -> bool:
    with MongoCon() as cnx:
        receptionist = cnx.users.find_one(
            {"_id": ObjectId(receptionist_id)})
        if not receptionist:
            return False
        if len(receptionist["doctors"]) > 1:
            result = cnx.users.update_one(
                {"_id": ObjectId(receptionist_id)},
                {
                    "$pull": {"doctors": ObjectId(doctor_id)}
                })
            return result.modified_count > 0
        result = cnx.users.delete_one({"_id": ObjectId(receptionist_id)})
    return result.deleted_count > 0
