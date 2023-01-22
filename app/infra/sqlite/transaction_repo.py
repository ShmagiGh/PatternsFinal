from typing import Protocol

from app.core.model.transaction_dto import TransactionDTO
from app.infra.sqlite.database import DB


class ITransactionRepository(Protocol):
    def create_transaction(self, transaction: TransactionDTO) -> None:
        pass

class TransactionRepository(ITransactionRepository):
    def __init__(self, db: DB) -> None:
        self.db = db

        self.db.cur.execute(
            """CREATE TABLE IF NOT EXISTS transactions
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount FLOAT NOT NULL,
                commision FLOAT NOT NULL DEFAULT 0,
                coin_type_id INTEGER NOT NULL,
                wallet_from_address TEXT NOT NULL,
                wallet_to_address TEXT NOT NULL,
                time_created DATETIME DEFAULT CURRENT_TIMESTAMP),
                FOREIGN KEY(wallet_from_address) REFERENCES wallets(address),
                FOREIGN KEY(wallet_to_address) REFERENCES wallets(address);"""
                #TODO: ეს უნდა მივაბა როცა ქოინების თეიბლი გვექნება
                # FOREIGN KEY(coin_type_id) REFERENCES wallets(address)
        )

        def create_transaction(self, transaction: TransactionDTO) -> None:
            self.db.cur.execute(
                """INSERT INTO transactions (amount,
                                             commision,
                                             coin_type_id,
                                             wallet_from_address,
                                             wallet_to_address) VALUES(?,?,?,?,?)""",
                (transaction.amount,
                 transaction.commission,
                 transaction.coin_type_id,
                 transaction.wallet_from_address,
                 transaction.wallet_to_address),
            )


