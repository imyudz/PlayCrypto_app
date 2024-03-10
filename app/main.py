from dotenv import load_dotenv
from fastapi import FastAPI

from presentation.routes.auth_router import auth_router
from presentation.routes.wallet_router import wallet_router

load_dotenv()

app = FastAPI(
    title="PlayCrypto API",
    description="API de acesso ao PlayCrypto",
)

app.include_router(auth_router)
app.include_router(wallet_router)


@app.get("/")
def root():
    return {"message": "Hello World"}