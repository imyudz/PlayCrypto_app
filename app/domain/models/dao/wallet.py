from pydantic import BaseModel, Field, validator
from decimal import Decimal
from typing import Annotated
from datetime import datetime
import pytz

class InsertWalletModel(BaseModel):
    last_modified: Annotated[str, Field(alias="last_modified")] = datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()
    wallet_name: Annotated[str, Field(alias="wallet_name")]
    dolar_balance: Annotated[Decimal, Field(alias="dolar_balance")]
    fk_user_id: Annotated[int, Field(alias="fk_user_id")]
    wallet_recovery_phrase_hash: Annotated[str, Field(alias="wallet_recovery_phrase_hash")]

class Wallet(InsertWalletModel):
    id: int = Field(alias="id")
    created_at: str = Field(alias="created_at")