import os
from domain.models.user import User, InsertUserModel
from services.repositories.interfaces.user_interface import UserInterface
from services.connectors.supabase_connector import SupabaseConnector
from pydantic import EmailStr
from fastapi.encoders import jsonable_encoder

class SupabaseUserRepository(UserInterface):
    def __init__(self) -> None:
        self.__client = SupabaseConnector(
            os.getenv("SUPABASE_URL"), 
            os.getenv("SUPABASE_ADMIN_KEY")).get_supabase_client()
        pass
    
    def get_user_by_email(self, email: EmailStr) -> User:
        query = self.__client.table("User").select("*").eq("email", email)
        try:
            result = query.execute()
            print(result)
            if len(result.data) == 0:
                return None
        except Exception as e:
            print(e)
            raise e
        return User(**result.data[0])
    
    def insert_user(self, user: InsertUserModel) -> bool:
        query = self.__client.table("User").insert(jsonable_encoder(user))
        try:
            query.execute()
        except Exception as e:
            raise e
        return True
    