import os
from services.connectors.coingecko_api_connector import (
    CoingeckoAPIConnector as __CoingeckoAPI,
)
from services.repositories.coins_repository import (
    SupabaseCoinsRepository as __SupabaseCoinsRepository,
)
from domain.models.dao.coins import Coins as __CoinsModel, InsertCoinsModel as _InsertCoinsModel
from domain.schemas.response_schemas.coin_response_schema import CGeckoCoinsListResponse as _CGeckoCoinsListResponse

__coingecko_url = os.getenv("COINGECKO_BASE_URL")
__coingecko_key = os.getenv("COINGECKO_API_KEY")

async def update_all_coins(webhook_request: dict) -> None:
    # Primeiro, busca as moedas existentes no banco
    try:        
        assert __coingecko_url and __coingecko_key, "expected 'COINGECKO_BASE_URL' and 'COINGECKO_API_KEY', but not found in .env"
        coingecko_api = __CoingeckoAPI(
            coingecko_url=__coingecko_url,
            coingecko_api_key=__coingecko_key,
        )
        coins_repository = __SupabaseCoinsRepository()
        response: list[_CGeckoCoinsListResponse] = await coingecko_api.get_coins_list()
        
        database_coins_list: list[__CoinsModel] = await coins_repository.get_coins()
        if len(database_coins_list) != 0:
            assert "currency" in webhook_request, "expected 'currency', but not found in webhook_request"
            new_coin_abr = webhook_request["currency"]
        
        print(response)
        
        # coin_list = []
        # for coin in response:
        #     coin_list.append(
        #         _InsertCoinsModel(
        #             coin_id_coingecko=coin.id
        #         )
        #     )
            

        
        

    except Exception as e:
        print("Erro ao atualizar as moedas existentes no banco", e)
        raise e
