from decimal import Decimal

from app.infra.in_memory.statistics_memory_repo import (
    InMemoryStatisticRepoWithSettableProfit,
)


def test_get_statistic() -> None:
    statistic_repo_test = InMemoryStatisticRepoWithSettableProfit(profit=Decimal(10))

    assert statistic_repo_test.get_commissions_of_all_transactions() == Decimal(10)
