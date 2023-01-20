from typing import Protocol

from database import DB

from app.core.model.coin import CoinDTO
from app.core.model.wallet_dto import WalletDTO


class IWalletRepository(Protocol):
    def create_wallet(self, wallet: WalletDTO) -> None:
        pass

    def deposit_to_wallet(
        self, wallet: WalletDTO, coin: CoinDTO, amount: float
    ) -> None:
        pass

    def withdraw_from_wallet(
        self, wallet: WalletDTO, coin: CoinDTO, amount: float
    ) -> None:
        pass

    def check_wallet_balance(self, wallet: WalletDTO, coin: CoinDTO) -> float:
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
                balance DOUBLE NOT NULL);"""
        )

        # self.db.cur.execute(
        #     """CREATE TABLE IF NOT EXISTS coins
        #         (id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         coin TEXT NOT NULL);"""
        # )

    def create_wallet(self, wallet: WalletDTO) -> None:
        self.db.cur.execute(
            """INSERT INTO wallets (api_key, address) VALUES(?,?)""",
            (wallet.api_key, wallet.address),
        )
        # self.db.conn.commit()

    def deposit_to_wallet(
        self, wallet: WalletDTO, coin: CoinDTO, amount: float
    ) -> None:
        self.db.cur.execute(
            """UPDATE balances
                  SET amount = amount + ?
                WHERE wallet_address = ?
                  AND coin_id = ?
              VALUES(?,?,?)""",
            (amount, wallet.address, coin.coin_id),
        )

    def withdraw_from_wallet(
        self, wallet: WalletDTO, coin: CoinDTO, amount: float
    ) -> None:
        self.db.cur.execute(
            """UPDATE balances
                  SET amount = amount - ?
                WHERE wallet_address = ?
                  AND coin_id = ?
              VALUES(?,?,?)""",
            (amount, wallet.address, coin.coin_id),
        )

    def check_wallet_balance(self, wallet: WalletDTO, coin: CoinDTO) -> float:
        balance = self.db.cur.execute(
            """SELECT balance 
                 FROM balances
                WHERE wallet_address = ?
                  AND coin_id = ?
               VALUES(?,?)""",
            (wallet.address, coin.coin_id),
        ).fetchone()[0]
        return balance

    # def add_coin_type(self, new_coin: str):
    #     self.db.cur.execute(
    #         """INSERT INTO coins (coin) VALUES(?)""",
    #         (new_coin, ),
    #     )
