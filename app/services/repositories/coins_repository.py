import os
from app.domain.models.dao.coins import InsertCoinsModel as _InsertCoinsModel, Coins as _CoinsModel
from services.repositories.interfaces.coins_interface import CoinsInterface as __CoinsInterface
from services.connectors.supabase_connector import SupabaseConnector
from fastapi.encoders import jsonable_encoder as __encoder
from postgrest import APIResponse as __ApiResponse

class SupabaseCoinsRepository(__CoinsInterface):
    def __init__(self) -> None:
        self.__client = SupabaseConnector(
            os.getenv("SUPABASE_URL"), 
            os.getenv("SUPABASE_ADMIN_KEY")).get_supabase_client()
    
    async def get_coins(self) -> list[_CoinsModel]:
        query = self.__client.table("Coins").select("*", count="exact")
        try:
            result: __ApiResponse = query.execute()
            print(f"\n\n ********* GET COINS RESULTADO: ********* \n {result} \n **************************** \n\n")
            return [_CoinsModel(**coin) for coin in result.data]
        except Exception as e:
            print("Erro ao buscar as moedas existentes no banco", e)
            raise e

    async def insert_coins(self, coins: list[_InsertCoinsModel] | _InsertCoinsModel) -> bool:
        query = self.__client.table("User").insert(__encoder(coins))
        try:
            result: __ApiResponse = query.execute()
            print(f"\n\n ********* INSERT COINS RESULTADO: ********* \n {result} \n **************************** \n\n")
        except Exception as e:
            print("Erro ao inserir moedas: ", e)
            return False
        return True