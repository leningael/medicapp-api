from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from api.middlewares.error_handler import ErrorHandler
from api.routers.user import user_router
from api.routers.calendar import calendar_router
from api.routers.patient import patient_router
from api.routers.receptionist import receptionist_router

app = FastAPI()
app.title = "MedicApp API"
app.version = "0.0.1"

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
# app.add_middleware(ErrorHandler)

app.include_router(user_router)
app.include_router(calendar_router)
app.include_router(patient_router)
app.include_router(receptionist_router)

@app.get("/")
def root():
    return {"message": "Welcome to MedicApp API"}