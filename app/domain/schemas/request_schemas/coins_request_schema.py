from pydantic import BaseModel

class CoinAlertRequest(BaseModel):
    type: str | None = None
    message: str | None = None
    currency: str | None = None
    exchange: str | None = None