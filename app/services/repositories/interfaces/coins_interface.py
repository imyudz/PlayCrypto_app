from typing import Generic, TypeVar
from app.domain.models.dao.coins import InsertCoinsModel
T = TypeVar('T')

class CoinsInterface(Generic[T]):
    def get_coins_count(self) -> T:
        raise NotImplementedError
    def insert_coins(self, coins: InsertCoinsModel) -> T:
        raise NotImplementedError
    
