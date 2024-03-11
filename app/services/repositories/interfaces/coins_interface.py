from typing import Generic, TypeVar
from app.domain.models.dao.coins import InsertCoinsModel
T = TypeVar('T')

class CoinsInterface(Generic[T]):
    def get_coins(self) -> T:
        def by_id(id: int) -> T:
            raise NotImplementedError
        def by_coingecko_id(coingecko_id: str) -> T:
            raise NotImplementedError
        raise NotImplementedError
    def insert_coins(self, coins: list[InsertCoinsModel] | InsertCoinsModel) -> T:
        raise NotImplementedError
    
