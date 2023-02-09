from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

from app.infra.sqlite.database import DB


class IStatisticRepository(Protocol):
    def get_commissions_of_all_transactions(self) -> Decimal:
        pass


@dataclass
class StatisticRepository(IStatisticRepository):
    db: DB

    def get_commissions_of_all_transactions(self) -> Decimal:
        try:
            transaction_str = """SELECT SUM(commision)
                                      FROM transactions;"""

            profit = self.db.cur.execute(
                transaction_str,
            ).fetchone()[0]

            return Decimal(profit)
        except Exception as e:
            print(e)
            return None
