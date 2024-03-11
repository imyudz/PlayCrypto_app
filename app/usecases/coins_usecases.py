import os

from domain.models.dao.coins import Coins as __CoinsModel
from domain.models.dao.coins import InsertCoinsModel as _InsertCoinsModel
from domain.schemas.request_schemas.coins_request_schema import \
    CoinAlertRequest as _CoinAlertRequest
from domain.schemas.response_schemas.coin_response_schema import \
    CGeckoCoinsListResponse as _CGeckoCoinsListResponse
from services.connectors.coingecko_api_connector import \
    CoingeckoAPIConnector as __CoingeckoAPI
from services.repositories.coins_repository import \
    SupabaseCoinsRepository as __SupabaseCoinsRepository
from utils.coins_utils import \
    extract_name_from_webhook_message as _extract_name

__coingecko_url = os.getenv("COINGECKO_BASE_URL")
__coingecko_key = os.getenv("COINGECKO_API_KEY")

__coingecko_api = __CoingeckoAPI(
            coingecko_url=__coingecko_url,
            coingecko_api_key=__coingecko_key,
        )

__coins_repository = __SupabaseCoinsRepository()
    

async def update_coins_by_webhook_alert(webhook_request: _CoinAlertRequest, verify_webhook_coin: bool = False) -> None:

    try:
        # Primeiro, busca as moedas existentes na base da coingecko  
        assert __coingecko_url and __coingecko_key, "expected 'COINGECKO_BASE_URL' and 'COINGECKO_API_KEY', but not found in .env"

        response: list[_CGeckoCoinsListResponse] = await __coingecko_api.get_coins_list()
        
        
        # Busca as moedas existentes no banco
        database_coins_list: list[__CoinsModel] = await __coins_repository.get_coins()
        
        # print(response)
        # print(database_coins_list)
        
        # Se tiver alguma moeda verifica no banco se ela já não existe, na api se ela existe, e pega os dados dela para inserção
        if len(database_coins_list) != 0:
            if verify_webhook_coin != False: 
                new_coin_name = _extract_name(webhook_request.message)
                new_coin_possible_id = new_coin_name.lower().replace(" ", "-")
                #verificar se o nome .lower e trocando os espaços por traço não é igual ao coin id da coingecko ou se o nome é igual ao coin name da coingecko ou do banco

                assert new_coin_name not in [coin.coin_name for coin in database_coins_list] and new_coin_possible_id not in [coin.coin_id_coingecko for coin in database_coins_list], "Coin already exists in database. Leaving..."
                coin_data = next((coin for coin in response if coin.name == new_coin_name or coin.id == new_coin_possible_id), None)
                assert coin_data is not None, f"Coin {new_coin_name} or {new_coin_possible_id} not found in Coingecko API. Leaving..."

                insertion = await __coins_repository.insert_coins(_InsertCoinsModel(
                    coin_abreviation=coin_data.symbol.upper(),
                    coin_name=coin_data.name,
                    coin_id_coingecko=coin_data.id
                ))
                if not insertion: raise ValueError("Failed to insert new coin")
                return
            
            print("Vejo as moedas que vieram na response e não vieram no banco e atualizo o banco com as moedas que não estão nele e vieram no response da api")
            # Vejo as moedas que vieram na response e não vieram no banco e atualizo o banco com as moedas que não estão nele e vieram no response da api
            new_coins_ids = {coin.id for coin in response} - {coin.coin_id_coingecko for coin in database_coins_list}
            if new_coins_ids:
                new_coins_list = [
                    _InsertCoinsModel(coin_id_coingecko=coin.id, coin_abreviation=coin.symbol.upper(), coin_name=coin.name)
                    for coin in response if coin.id in new_coins_ids
                ]
                insertion = await __coins_repository.insert_coins(new_coins_list)
                if not insertion: raise ValueError("Failed to update coins")
            else:
                print("All coins already updated")
            return
        
        # Se não tiver nenhuma moeda faz a inserção com todas as moedas da coingecko
        coin_list: list[_InsertCoinsModel] = []
        for coin in response:
            coin_list.append(
                _InsertCoinsModel(
                    coin_id_coingecko=coin.id,
                    coin_abreviation=coin.symbol.upper(),
                    coin_name=coin.name
                )
            )
        insertion = await __coins_repository.insert_coins(coin_list)
        
    except Exception as e:
        print("Erro ao atualizar as moedas existentes no banco", e)
        raise e

async def get_coins_list() -> list[__CoinsModel]:
    try:
        coins = await __coins_repository.get_coins()
        return coins
    except Exception as e:
        print("Error while getting coins list", e)
        raise e
    