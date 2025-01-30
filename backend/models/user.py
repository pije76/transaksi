from fastapi import FastAPI, File, UploadFile, APIRouter, Depends, HTTPException, Security, Form, status

from pydantic import BaseModel, ConfigDict, EmailStr, Field, validator
from pydantic.types import SecretStr, constr
from typing import Optional, List, Annotated, Literal, Union, TYPE_CHECKING

# from datetime import datetime

from backend.validator import *
from backend.auth import oauth2_scheme

# if TYPE_CHECKING:
#     from models.transaction import TransactionLog

class User(BaseModel):
    username: str
    password: str
    email: Union[EmailStr, Literal[""]] | None = None

class UpdateUser(User):
    # payment_method: Literal['bank', 'emoney'] | None = None
    payment_method: Optional[Literal['bank', 'emoney']] = None
    # payment_number: int | None = None
    payment_number: Optional[int] = None
    # photo: str | None = None
    photo: Optional[str] = None

class UserRole(BaseModel):
    name: str

    @validator('name')
    def name_must_be_valid(cls, value):
        allowed_roles = ['admin', 'regular']
        if value.lower() not in allowed_roles:
            raise ValueError(
                f"Invalid role. Allowed roles are: {', '.join(allowed_roles)}"
            )
        return value

class Authorization:

    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
        # auth_service: AuthService = Depends(get_auth_service),
    ):
        user_data = auth_service.get_current_user(token)
        if not user_data or user_data.role not in [role.name for role in self.allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='This operation is forbidden for you',
            )

        return user_data

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
