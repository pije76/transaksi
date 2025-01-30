from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from passlib.context import CryptContext
from string import ascii_lowercase, ascii_uppercase, digits, punctuation

import re

PASSWORD_RE = re.compile(r"[A-Za-z\d/+=]{44}")
NAME_RE = re.compile(r"[A-Za-zА-яЁё\d]")

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 24

ASCII_LOWERCASE = set(ascii_lowercase)
ASCII_UPPERCASE = set(ascii_uppercase)
DIGITS = set(digits)
PUNCTUATION = set(punctuation)
AVAILABLE_CHARS = ASCII_LOWERCASE | ASCII_UPPERCASE | DIGITS | PUNCTUATION

MAX_NAME_LEN = 100
MIN_NAME_LEN = 3

security = HTTPBasic()
hash_helper = CryptContext(schemes=["bcrypt"])

async def validate_login(credentials: HTTPBasicCredentials = Depends(security)):
    admin = admin_collection.find_one({"email": credentials.username})
    if admin:
        password = hash_helper.verify(credentials.password, admin['password'])
        if not password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        return True
    return False


def validate_password(password: str) -> str | ValueError:
    if re.search(PASSWORD_RE, password):
        return password
    password_chars = set(password)
    if not (
        (MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH)
        and (password_chars & ASCII_LOWERCASE)
        and (password_chars & ASCII_UPPERCASE)
        and (password_chars & DIGITS)
        and (password_chars & PUNCTUATION)
        and not (password_chars - AVAILABLE_CHARS)
    ):
        raise ValueError(
            "Invalid validate password",
        )
    return password


def validate_name(name: str | None = None) -> str | None | ValueError:
    if not name:
        return None
    if len(name) < MIN_NAME_LEN:
        raise ValueError(
            f"Name field average min symbols :: {MIN_NAME_LEN}",
        )
    if len(name) > MAX_NAME_LEN:
        raise ValueError(
            f"Name field average max symbols :: {MAX_NAME_LEN}",
        )
    if not bool(re.search(NAME_RE, name)):
        raise ValueError(
            "Invalid symbols in name field",
        )
    return name
