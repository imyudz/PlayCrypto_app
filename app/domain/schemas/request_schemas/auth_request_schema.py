from pydantic import BaseModel

class UserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str