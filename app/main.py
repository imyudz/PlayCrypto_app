import os
from datetime import datetime, timedelta, timezone
from typing import Annotated
from dotenv import load_dotenv
from fastapi import FastAPI

from presentation.routes.auth_router import auth_router

load_dotenv()

app = FastAPI(
    title="PlayCrypto API",
    description="API de acesso ao PlayCrypto",
)

app.include_router(auth_router)


# class TokenData(BaseModel):
#     username: str | None = None

# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None
    
# class dbUser(User):
#     hashed_password: str


# password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




# def verify_password(plain_password, hashed_password):
#     return password_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return password_context.hash(password)

# def get_user(supabaseClient: Client, userMail: str):   #repository
#     supabaseClient.table("User").select("email")       #repository
#     if username in db:                                 #repository
#         user_dict = db[username]                       #repository
#         return dbUser(**user_dict)                     #repository
    
# def authenticate_user(database: Client, usermail:str, password: str):
#     user = get_user(fake_db, usermail)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# def fake_hash_password(password: str):
#     return "fakehashed" + password



    



# @app.post("/token")
# async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"}
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return Token(access_token=access_token, token_type="bearer")
        


@app.get("/")
def root():
    return {"message": "Hello World"}