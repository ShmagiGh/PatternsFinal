from dataclasses import dataclass
from typing import Protocol
from decimal import Decimal

from app.infra.sqlite.database import DB


class IStatisticRepository(Protocol):
    def get_commissions_of_all_transactions(self) -> Decimal:
        pass

@dataclass
class StatisticRepository(IStatisticRepository):
    db: DB
    def get_commissions_of_all_transactions(self) -> Decimal:
        transaction_str = """SELECT SUM(commision)
                                  FROM transactions;"""

        profit = self.db.cur.execute(
            transaction_str,
        ).fetchone()[0]

        return Decimal(profit)
