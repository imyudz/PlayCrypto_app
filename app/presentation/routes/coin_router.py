from fastapi import APIRouter as __APIRouter, status as __status, BackgroundTasks as __BackgroundTasks
from fastapi.responses import JSONResponse as __JSONResponse
from domain.schemas.request_schemas.coins_request_schema import CoinAlertRequest as __CoinAlertRequest
from domain.schemas.response_schemas.coin_response_schema import CoinsListResponseModel as __CoinsListResponse
from usecases.coins_usecases import update_coins_by_webhook_alert as __update_all_coins

coin_router = __APIRouter(
    prefix="/coin",
    tags=["Coin Routes"],
)

@coin_router.post("/new-coin-alert")
def webhook_coin_alert(message: __CoinAlertRequest, background_tasks: __BackgroundTasks) -> __JSONResponse:
    print("Mensagem recebida: ", message)
    try:
        if message.type == "new_coin":
            background_tasks.add_task(__update_all_coins, message, False)
    except Exception as e:
        return __JSONResponse(status_code=__status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))
    return __JSONResponse(status_code=__status.HTTP_200_OK, content="OK")


@coin_router.get("/list", response_model=__CoinsListResponse)
def get_all_coins() -> __CoinsListResponse:
    return __CoinsListResponse(results=__update_all_coins(None, True))