from dataclasses import dataclass
from decimal import Decimal

from app.infra.sqlite.statistic_repo import IStatisticRepository


@dataclass
class InMemoryStatisticRepoWithSettableProfit(IStatisticRepository):
    profit: Decimal

    def get_commissions_of_all_transactions(self) -> Decimal:
        return self.profit
