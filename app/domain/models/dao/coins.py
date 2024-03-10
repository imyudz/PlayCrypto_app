from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime
import pytz

class InsertCoinsModel(BaseModel):
    last_modified: Annotated[str, Field(alias="last_modified")] = datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()
    coin_id_coingecko: Annotated[str, Field(alias="coin_id_coingecko")]
    coin_name: Annotated[str, Field(alias="coin_name")]
    coin_abreviation: Annotated[str, Field(alias="coin_abreviation")]

class Coins(InsertCoinsModel):
    id: Annotated[int, Field(alias="id")]