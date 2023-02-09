from dataclasses import dataclass
from typing import Protocol

from app.core.model.coin_dto import CoinDTO
from app.infra.sqlite.coin_repo import ICoinRepository


class ICoin(Protocol):
    def find_coin_by_id(self, coin_id: int) -> CoinDTO | None:
        pass

    def find_coin_by_name(self, name: str) -> CoinDTO | None:
        pass


@dataclass
class CoinService(ICoin):
    _coin_repo: ICoinRepository

    def find_coin_by_id(self, coin_id: int) -> CoinDTO | None:
        return self._coin_repo.find_coin_by_id(coin_id)

    def find_coin_by_name(self, name: str) -> CoinDTO | None:
        return self._coin_repo.find_coin_by_name(name)
