from typing import Generic, TypeVar
from app.domain.models.dao.user import InsertUserModel
T = TypeVar('T')

class UserInterface(Generic[T]):
    def get_user_by_email(self, email: str) -> T:
        raise NotImplementedError
    def insert_user(self, user: InsertUserModel) -> T:
        raise NotImplementedError
    
