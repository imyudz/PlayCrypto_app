from fastapi import APIRouter, Security
from fastapi.responses import JSONResponse
from dependencies.auth_dependencies import oauth2_scheme


wallet_router = APIRouter(
    prefix="/wallets",
    tags=["Wallet Routes"],
    dependencies=[Security(oauth2_scheme, scopes=["wallet"])],
)


@wallet_router.post("/create", name="create-wallet")
async def create_wallet( ):
    return "ok"

