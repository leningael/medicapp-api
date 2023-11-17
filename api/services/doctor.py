from typing import List
from bson import ObjectId
from api.schemas.doctor import DoctorOverview
from config.mongoCon import MongoCon


def get_receptionist_doctors(receptionist_id: str, search: str = None) -> List[DoctorOverview]:
    with MongoCon() as cnx:
        doctors = list(cnx.users.aggregate([
            {
                '$match': {
                    '_id': ObjectId(receptionist_id)
                }
            },
            {
                '$lookup': {
                    'from': 'users',
                    'localField': 'doctors',
                    'foreignField': '_id',
                    'as': 'doctors'
                }
            },
            {
                '$unwind': {
                    'path': '$doctors'
                }
            },
            {
                '$match': ({
                    "$or": [
                        {"doctors.name": {"$regex": search, "$options": "i"}},
                        {"doctors.lastname": {"$regex": search, "$options": "i"}}
                    ]
                } if search else {})
            },
            {
                '$replaceRoot': {
                    'newRoot': '$doctors'
                }
            },
            {
                '$project': {
                    'name': 1,
                    'lastname': 1,
                    'email': 1,
                }
            }
        ]))
    return doctors
    