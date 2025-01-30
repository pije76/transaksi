from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from backend.connection import *
# from backend.controllers.user import *
# from backend.models.user import *

pwd_context = CryptContext(schemes =["bcrypt"], deprecated="auto")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token", scheme_name="JWT")


# fake_users_db = {
#     "pije76": {
#         "username": "pije76",
#         "password": "$2b$12$6PfeGle9/RVAyMfzs8e.quzBbYoLszsxyMf7UZAA4PGCy6L9qP4eC",
#         "email": "pije76@yahoo.com",
#         # "disabled": False,
#     },
# }


class Hash():
    def bcrypt(password: str):
        print("pwd_context", pwd_context)
        print("pwd_context.hash(password)", pwd_context.hash(password))
        return pwd_context.hash(password)
    # def verify(normal, hashed):
    def verify(hashed, normal):
        print("pwd_context", pwd_context)
        print("hashed", hashed)
        print("normal", normal)
        return pwd_context.verify(normal, hashed)
        print("pwd_context.verify(normal, hashed)", pwd_context.verify(normal, hashed))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception


# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         # return UserInDB(**user_dict)
#         return User(**user_dict)


def get_current_user(token: str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("payload", payload)
        username: str = payload.get("sub")
        print("username", username)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = user_collection.find_one({"username": username})
    print("user", user)
    if user is None:
        raise credentials_exception
    return user

# def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# def check_roles(roles: List[str]):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             # Get the current user's roles from the database or token
#             # Check if any of the roles match the required roles
#             # If not, raise an HTTPException with 403 status code
#             # Else, continue with the execution of the function
#             return func(*args, **kwargs)
#         return wrapper
#     return decorator

class MyException(Exception):
    def __init__(self, item_id: str):
        self.item_id = item_id

