from fastapi import FastAPI, File, UploadFile, APIRouter, Depends, HTTPException, Security, Form, status

from pydantic import BaseModel, ConfigDict, EmailStr, Field, validator
from pydantic.types import SecretStr, constr
from typing import Optional, List, Annotated, Literal, Union, TYPE_CHECKING

from backend.auth import oauth2_scheme


class User(BaseModel):
    username: str
    password: str
    email: Union[EmailStr, Literal[""]] | None = None

class UpdateUser(User):
    payment_method: Optional[Literal['bank', 'emoney']] = None
    payment_number: Optional[int] = None
    photo: Optional[str] = None


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
