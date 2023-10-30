
from fastapi import APIRouter
from fastapi import status
from fastapi import HTTPException
from fastapi import Depends


from api.services.notes import NotesService
from api.schemas.notes import Notes

notes_router = APIRouter(tags=["notes"],prefix='/note')

@notes_router.get("/")
def index():
    notes = NotesService.get_notes()
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Notes not found")
    return notes


