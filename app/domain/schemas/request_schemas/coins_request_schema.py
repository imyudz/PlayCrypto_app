from pydantic import BaseModel

class CoinAlertRequest(BaseModel):
    type: str
    message: str
    currency: str
    exchange: str