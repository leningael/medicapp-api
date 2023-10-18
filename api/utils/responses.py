from fastapi import status
from fastapi.responses import JSONResponse
from datetime import date, datetime
from bson import ObjectId
from fastapi.encoders import jsonable_encoder


ENCODERS = {
    ObjectId: lambda vl: str(vl),
    date: lambda vl: datetime.strftime(vl, r"%b %d %Y"),
    datetime: lambda vl: date.strftime(vl, r"%b %d %Y %H:%M")
}

def json_encoder(obj, *args, **kwargs):
    return jsonable_encoder(
        obj, 
        *args, 
        **kwargs, 
        custom_encoder=ENCODERS
    )

def success_ok():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "success"})


def not_found(item=""):
    return JSONResponse(
        {"message": f"{item} not found"}, status_code=status.HTTP_404_NOT_FOUND
    )


def error_params_required(params=None):
    message = {param: 'Required field not found' for param in params}
    return jsonable_encoder({"message": message}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)