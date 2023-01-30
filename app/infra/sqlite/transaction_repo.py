import enum
from typing import Protocol, List

from app.core.model.transaction_dto import TransactionDTO
from app.core.model.wallet_dto import WalletDTO
from app.infra.sqlite.database import DB


class AddressType(enum.Enum):
   from_wallet = "wallet_from_address"
   to_wallet = "wallet_to_address"

class ITransactionRepository(Protocol):
    def create_transaction(self, transaction: TransactionDTO) -> None:
        pass

    def get_transactions_of_user(self, api_key: str) -> List[TransactionDTO]:
        pass

    def get_transactions_sent(self, address: str) -> List[TransactionDTO]:
        pass

    def get_transactions_received(self, address: str) -> List[TransactionDTO]:
        pass

# TODO: Need to recheck and finish
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
            # TODO: ეს უნდა მივაბა როცა ქოინების თეიბლი გვექნება
            # FOREIGN KEY(coin_type_id) REFERENCES wallets(address)
        )

        def create_transaction(self, transaction: TransactionDTO) -> None:
            self.db.cur.execute(
                """INSERT INTO transactions (amount,
                                             commision,
                                             coin_type_id,
                                             wallet_from_address,
                                             wallet_to_address)
                                VALUES(?,?,?,?,?)""",
                (
                    transaction.amount,
                    transaction.commission,
                    transaction.coin_type_id,
                    transaction.wallet_from_address,
                    transaction.wallet_to_address,
                ),
            )

        def get_transactions_of_user(self, api_key: str) -> List[TransactionDTO]:
          pass

        def get_transactions_sent(self, address: str) -> List[TransactionDTO]:
            self._get_transaction(address=address, address_type=AddressType.to_wallet)

        def get_transactions_received(self, address: str) -> List[TransactionDTO]:
            self._get_transaction(address=address,address_type=AddressType.from_wallet)

        def _get_transaction(self, address: str, address_type: AddressType) -> List[TransactionDTO]:
            transactions = self.db.cur.execute(
                """SELECT (amount,
                           commision,
                           coin_type_id,
                           wallet_from_address,
                           wallet_to_address)
                     FROM transactions
                    WHERE ? = ? 
                """,
                (address_type.value, address),
            ).fetchall()

            transactions = map(lambda elem: TransactionDTO(amount=elem[0],
                                                           commission=elem[1],
                                                           coin_type_id=elem[2],
                                                           wallet_from_address=elem[3],
                                                           wallet_to_address=elem[4]), transactions)
            return transactions

