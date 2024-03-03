import os
from supabase import create_client, Client
from supabase.client import ClientOptions

class SupabaseConnector:
    def __init__(self, url, key) -> None:
        self.session = None
        self.token = None
        self.__SUPABASE_URL: str = url
        self.__SUPABASE_KEY: str = key
        self.__supabase: Client = create_client(self.__SUPABASE_URL, self.__SUPABASE_KEY,
            options=ClientOptions(
                postgrest_client_timeout=10,
                storage_client_timeout=10
            ))

    def get_supabase_client(self):
        return self.__supabase
    
    def login(self, email, pwd) -> str:
        try:
            print(email, pwd)
            
            self.session = self.__supabase.auth.sign_in_with_password({ "email": email, "password": pwd })
            assert self.session != None
    
            try:
                client = self.__supabase.postgrest.auth(self.session.session.access_token)
                return client
            except Exception as e:
                raise e
            
        except Exception as e:
            print("Falha ao logar:", e)
            raise e
            
            
            