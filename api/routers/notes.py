
from fastapi import APIRouter
from fastapi import status
from fastapi import HTTPException
from fastapi import Depends
from fastapi.encoders import jsonable_encoder


from api.services.notes import NotesService
from api.schemas.notes import NoteContent, NoteOverview, Note

notes_router = APIRouter(tags=["notes"],prefix='/note')

@notes_router.get("/")
def index():
    notes = NotesService().get_notes()
    return jsonable_encoder(notes)

@notes_router.post("/")
def create_note(note: Note):
    response = NotesService().post_note(note)
    return response

@notes_router.get("/{id}")
def delete_note(id: str):
    response = NotesService().get_details(id)
    content = response.pop('content', False)
    return jsonable_encoder({**response, **content})

@notes_router.delete("/{id}")
def delete_note(id: str):
    response = NotesService().delete_note(id)
    return response

@notes_router.put("/{id}")
def update_note(id: str, note: Note):
    response = NotesService().update_note(id, note)
    return response