from decimal import Decimal
from typing import Protocol

from app.core.model.wallet_dto import WalletDTO
from app.infra.sqlite.database import DB


class IWalletRepository(Protocol):
    def create_wallet(self, wallet: WalletDTO, coin_id: int, amount: Decimal) -> None:
        pass

    def deposit_to_wallet(
        self, wallet: WalletDTO, coin_id: int, amount: Decimal
    ) -> None:
        pass

    def withdraw_from_wallet(
        self, wallet: WalletDTO, coin_id: int, amount: Decimal
    ) -> None:
        pass

    def check_wallet_balance(self, wallet: WalletDTO, coin_id: int) -> Decimal:
        pass

    def check_wallet_count(self, api_key: str) -> int:
        pass

    def get_wallets(self, api_key: str) -> list[WalletDTO]:
        pass


class WalletRepository(IWalletRepository):
    def __init__(self, db: DB) -> None:
        self.db = db

        self.db.cur.execute(
            """CREATE TABLE IF NOT EXISTS wallets
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_key TEXT NOT NULL,
                address TEXT NOT NULL);"""
        )

        self.db.cur.execute(
            """CREATE TABLE IF NOT EXISTS balances
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                wallet_address TEXT NOT NULL,
                coin_id INTEGER NOT NULL,
                balance TEXT NOT NULL);"""
        )

        self.db.conn.commit()

        # self.db.cur.execute(
        #     """CREATE TABLE IF NOT EXISTS coins
        #         (id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         coin TEXT NOT NULL);"""
        # )

    def create_wallet(
        self,
        wallet: WalletDTO,
        coin_id: int = 1,
        amount: Decimal = Decimal("1"),
    ) -> None:
        self.db.cur.execute(
            """INSERT INTO wallets (api_key, address) VALUES(?,?)""",
            (wallet.api_key, wallet.address),
        )
        self.db.cur.execute(
            """INSERT INTO balances (wallet_address, coin_id, balance) VALUES(?,?,?)""",
            (wallet.address, coin_id, str(amount)),
        )
        self.db.conn.commit()

    def deposit_to_wallet(
        self, wallet: WalletDTO, coin_id: int, amount: Decimal
    ) -> None:
        curr_balance = self.check_wallet_balance(wallet, coin_id)
        new_balance = curr_balance + amount
        self.db.cur.execute(
            """UPDATE balances
                  SET balance = ?
                WHERE wallet_address = ?
                  AND coin_id = ?
            """,
            (str(new_balance), wallet.address, coin_id),
        )
        self.db.conn.commit()

    def withdraw_from_wallet(
        self, wallet: WalletDTO, coin_id: int, amount: Decimal
    ) -> None:
        curr_balance = self.check_wallet_balance(wallet, coin_id)
        new_balance = curr_balance - amount
        # print(curr_balance, amount, curr_balance - amount, curr_balance + amount)
        # diff = curr_balance - amount
        # print(diff)
        self.db.cur.execute(
            """UPDATE balances
                  SET balance = ?
                WHERE wallet_address = ?
                  AND coin_id = ?
            """,
            (str(new_balance), wallet.address, coin_id),
        )
        self.db.conn.commit()

    def check_wallet_balance(self, wallet: WalletDTO, coin_id: int) -> Decimal:
        try:
            balance = self.db.cur.execute(
                """SELECT b.balance
                     FROM balances b
                     WHERE b.wallet_address = ?
                      AND b.coin_id = ?
                   """,
                (wallet.address, coin_id),
            ).fetchone()[0]
            return Decimal(str(balance))
        except Exception as e:
            print(e)
            return None

    def check_wallet_count(self, api_key: str) -> int:
        count = self.db.cur.execute(
            """SELECT COUNT(*)
                 FROM wallets
                WHERE api_key = ?
            """,
            (api_key,),
        ).fetchone()[0]
        return count

    def get_wallets(self, api_key: str) -> list[WalletDTO]:
        wallets = self.db.cur.execute(
            """SELECT api_key, address
                 FROM wallets
                WHERE api_key = ?
            """,
            (api_key,),
        ).fetchall()
        return_wallets = []
        for wallet in wallets:
            return_wallets.append(WalletDTO(wallet[0], wallet[1]))
        return return_wallets

    # def add_coin_type(self, new_coin: str):
    #     self.db.cur.execute(
    #         """INSERT INTO coins (coin) VALUES(?)""",
    #         (new_coin, ),
    #     )
