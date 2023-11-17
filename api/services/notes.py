from datetime import datetime
from bson import ObjectId
from api.schemas.notes import NoteContent, NoteOverview, Note
from config.mongoCon import MongoCon
from typing import List, Union
from fastapi import Body, HTTPException, status
from fastapi.encoders import jsonable_encoder

messages = {
    "not_found": "Note not found",
}

class NotesService:

    def get_notes(self,term: Union[None, str] = None):
        results = []
        notes = []
        with MongoCon() as cnx:
            if term is None:
                notes = cnx.notes.find()
                results = []
            else:
                search = {"$regexp": {"$search": term, "$options":"i"}}
                notes = cnx.notes.find({"$or": [{"title": search}, {"content.reason": search}]})
            for note in notes:
                note["_id"] = str(note["_id"])
                if note.get("content",False):
                    note["reason"] = note.get("content").get("reason")
                results.append(NoteOverview(**note))
        return results
    
    def get_details(self, id: Union[str, None]= None):
        if id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="ID must be defined")
        with MongoCon() as cnx:
            note = cnx.notes.find_one({"_id": ObjectId(id)})
            if not note:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=messages["not_found"])
            note["_id"] = str(note["_id"])
            return Note(**note)

    def get_appointment_note(self,appointment_id: Union[str, None]= None)-> Note:
        with MongoCon() as cnx:
            note_found = cnx.notes.find_one({"appointment_id": appointment_id})
            if not note_found:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=messages["not_found"])
            note_found["_id"] = str(note_found["_id"])
        return Note(**note_found)
    
    def post_note(self, note: Note):
        with MongoCon() as cnx:
            note = note.model_dump(exclude_none=True, exclude_unset=True, exclude_defaults=True, by_alias=True)
            note["patient"]["_id"] = str(note["patient"].pop('_id', ''))
            note_insert = cnx.notes.insert_one({**note})
        return jsonable_encoder({"id": str(note_insert.inserted_id), **note})
    
    def delete_note(cls, id: str):
        with MongoCon() as cnx:
            found = cnx.notes.find_one({"_id": ObjectId(id)})
            if not found:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=messages["not_found"])
            cnx.notes.delete_one({"_id": ObjectId(id)})
        return jsonable_encoder({"id": id, "message": "Note deleted successfully"})

    def update_note(cls, id: str, note: Note):
        with MongoCon() as cnx:
            note_model = note.model_dump(by_alias=True)
            del note_model["_id"]
            found = cnx.notes.find_one({"_id": ObjectId(id)})
            if not found:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=messages["not_found"])
            cnx.notes.update_one({"_id": ObjectId(id)}, {"$set":{**note_model}}, upsert=False)
        return jsonable_encoder({"id": id, "message": "Note update successfully"})
        
