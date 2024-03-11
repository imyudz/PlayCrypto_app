import os
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from services.repositories.user_repository import SupabaseUserRepository
from app.domain.models.dao.user import User
from domain.schemas.response_schemas.auth_response_schema import _TokenResponse
from fastapi.encoders import jsonable_encoder

SECRET_KEY = os.environ.get("JWT_SECRET")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_token(user: User) -> _TokenResponse | None:
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = __create_access_token(
        token_data=jsonable_encoder({"sub": user.email, "role": user.role}), expires_delta=access_token_expires
    )
    return _TokenResponse(access_token=access_token, token_type="bearer")

def __create_access_token(token_data: dict, expires_delta: timedelta | None = None):
    to_encode = token_data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

def encrypt_password(password):
    return password_context.hash(password)
    
def authenticate_user(useremail:str, password: str) -> User | None:
    user: User = SupabaseUserRepository().get_user_by_email(useremail)
    print(user)
    if not user:
        raise None
    if not verify_password(password, user.password_hash):
        return None
    return user
