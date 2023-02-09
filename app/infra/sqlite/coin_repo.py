from typing import Protocol

from app.core.model.coin_dto import CoinDTO
from app.infra.sqlite.database import DB


class ICoinRepository(Protocol):
    def find_coin_by_id(self, coin_id: int) -> CoinDTO | None:
        pass

    def find_coin_by_name(self, name: str) -> CoinDTO | None:
        pass


class CoinRepository(ICoinRepository):
    def __init__(self, db: DB) -> None:
        self.db = db
        self.db.cur.execute(
            """CREATE TABLE IF NOT EXISTS coins
                    (id INTEGER PRIMARY KEY NOT NULL,
                    coin TEXT NOT NULL);"""
        )
        self.db.conn.commit()

    def find_coin_by_id(self, coin_id: int) -> CoinDTO | None:
        try:
            coin = self.db.cur.execute(
                """SELECT id
                        FROM coins
                        WHERE id = ?""",
                (coin_id,),
            ).fetchone()[0]
            return coin
        except Exception as e:
            print(e)
            return None

    def find_coin_by_name(self, name: str) -> CoinDTO | None:
        try:
            coin = self.db.cur.execute(
                """SELECT id
                        FROM coins
                        WHERE coin = ?""",
                (name,),
            ).fetchone()[0]
            return coin
        except Exception as e:
            print(e)
            return None
