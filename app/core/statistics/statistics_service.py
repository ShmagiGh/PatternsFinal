from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

from app.infra.sqlite.statistic_repo import IStatisticRepository


class IStatistic(Protocol):
    def get_commissions_of_all_transactions(self) -> Decimal:
        pass


@dataclass
class StatisticService(IStatistic):
    statistic_repo: IStatisticRepository

    def get_commissions_of_all_transactions(self) -> Decimal:
        return self.statistic_repo.get_commissions_of_all_transactions()
