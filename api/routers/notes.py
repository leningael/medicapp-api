
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
    try:
        response = NotesService().post_note(note)
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@notes_router.get("/{id}")
def get_details(id: str):
    response = NotesService().get_details(id).model_dump(by_alias=True)
    content = response.pop('content', False)
    return jsonable_encoder({**response, **content})

@notes_router.delete("/{id}")
def delete_note(id: str):
    response = NotesService().delete_note(id)
    return response

@notes_router.put("/{id}")
def update_note(id: str, note: Note):
    try:
        response = NotesService().update_note(id, note)
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
   