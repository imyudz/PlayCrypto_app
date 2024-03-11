import os
from app.domain.models.dao.coins import InsertCoinsModel as _InsertCoinsModel, Coins as _CoinsModel
from services.repositories.interfaces.coins_interface import CoinsInterface as __CoinsInterface
from services.connectors.supabase_connector import SupabaseConnector
from fastapi.encoders import jsonable_encoder as _encoder
from postgrest import APIResponse as __ApiResponse

class SupabaseCoinsRepository(__CoinsInterface):
    def __init__(self) -> None:
        self.__client = SupabaseConnector(
            os.getenv("SUPABASE_URL"), 
            os.getenv("SUPABASE_ADMIN_KEY")).get_supabase_client()
    
    async def get_coins(self) -> list[_CoinsModel]:
        def by_id(id: int) -> _CoinsModel:
            query = self.__client.table("Coins").select("*").filter("id", "eq", id).limit(1)
            try:
                result: __ApiResponse = query.execute()
                assert len(result.data) > 0, "Coin not found"
                return _CoinsModel(**result.data[0])
            except Exception as e:
                raise e
        
        def by_coingecko_id(coingecko_id: str) -> _CoinsModel:
            query = self.__client.table("Coins").select("*").filter("coin_id_coingecko", "eq", coingecko_id).limit(1)
            try:
                result: __ApiResponse = query.execute()
                assert len(result.data) > 0, "Coin not found"
                return _CoinsModel(**result.data[0])
            except Exception as e:
                raise e

        query = self.__client.table("Coins").select("*", count="exact")
        try:
            result: __ApiResponse = query.execute()
            return [_CoinsModel(**coin) for coin in result.data]
        except Exception as e:
            print("Erro ao buscar as moedas existentes no banco", e)
            raise e
        
    async def insert_coins(self, coins: list[_InsertCoinsModel] | _InsertCoinsModel) -> bool:
        query = self.__client.table("Coins").insert(_encoder(coins))
        try:
            result: __ApiResponse = query.execute()
        except Exception as e:
            print("Erro ao inserir moedas: ", e)
            return False
        return True