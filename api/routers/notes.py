
from fastapi import APIRouter
from fastapi import status
from fastapi import HTTPException
from fastapi import Depends


from api.middlewares import jwt_bearer
from api.services.notes import NotesService
from api.schemas.notes import Notes

notes = APIRouter(tags=["notes"],prefix='/note')

@notes.get("/")
def index():
    notes = NotesService().get_notes()
    return notes


