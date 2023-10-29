from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.middlewares.error_handler import ErrorHandler
from api.routers import user, patient


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

app.include_router(user.router)
app.include_router(patient.router)


@app.get("/")
def root():
    return {"message": "Welcome to MedicApp API"}