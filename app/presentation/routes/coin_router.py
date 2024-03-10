from fastapi import APIRouter

coin_router = APIRouter(
    prefix="/coins",
    tags=["Coin Routes"],
)

@coin_router.post("/new-coin")
def webhook_receive_coin(message: dict):
    return
    