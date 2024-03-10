import os
from app.domain.models.dao.coins import InsertCoinsModel as __InsertCoinsModel, Coins as __CoinsModel
from services.repositories.interfaces.coins_interface import CoinsInterface as __CoinsInterface
from services.connectors.supabase_connector import SupabaseConnector as __Supabase
from fastapi.encoders import jsonable_encoder as __encoder

class SupabaseCoinsRepository(__CoinsInterface):
    def __init__(self) -> None:
        self.__client = __Supabase(
            os.getenv("SUPABASE_URL"), 
            os.getenv("SUPABASE_ADMIN_KEY")).get_supabase_client()
    
    async def get_coins_count(self) -> int:
        query = self.__client.table("Coins").select("*", count='exact')
        try:
            result = await query.execute()
            print(result)
            return result.count
        except Exception as e:
            print("Erro ao buscar as moedas existentes no banco", e)
            return 0

    async def insert_coins(self, coins: __InsertCoinsModel) -> bool:
        query = self.__client.table("User").insert(__encoder(coins))
        try:
            result = await query.execute()
            print(result)
        except Exception as e:
            print("Erro ao inserir moedas: ", e)
            return False
        return True