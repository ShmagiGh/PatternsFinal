import enum
from decimal import Decimal
from typing import List, Protocol

from app.core.model.transaction_dto import TransactionDTO
from app.core.model.wallet_dto import WalletDTO
from app.infra.sqlite.database import DB
from app.infra.sqlite.wallet_repo import WalletRepository


class AddressType(enum.Enum):
    from_wallet = "wallet_from_address"
    to_wallet = "wallet_to_address"


class ITransactionRepository(Protocol):
    def create_transaction(
        self, api_key: str, transaction: TransactionDTO
    ) -> TransactionDTO | None:
        pass

    def get_transactions_of_user(self, api_key: str) -> List[TransactionDTO]:
        pass

    def get_transactions_sent(self, address: str) -> List[TransactionDTO]:
        pass

    def get_transactions_received(self, address: str) -> List[TransactionDTO]:
        pass


class TransactionRepository(ITransactionRepository):
    def __init__(self, db: DB, wallet_repo: WalletRepository) -> None:
        self.db = db
        self.wallet_repo = wallet_repo
        self.db.cur.execute(
            """CREATE TABLE IF NOT EXISTS transactions
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount FLOAT NOT NULL,
                commision FLOAT NOT NULL DEFAULT 0,
                coin_type_id INTEGER NOT NULL,
                wallet_from_address TEXT NOT NULL,
                wallet_to_address TEXT NOT NULL,
                time_created DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(wallet_from_address) REFERENCES wallets(address),
                FOREIGN KEY(wallet_to_address) REFERENCES wallets(address));"""
        )
        self.db.conn.commit()

    def create_transaction(
        self, api_key: str, transaction: TransactionDTO
    ) -> TransactionDTO | None:
        wallet_from = WalletDTO(
            api_key=api_key, address=transaction.wallet_from_address
        )
        wallet_to = WalletDTO(api_key=api_key, address=transaction.wallet_to_address)

        coin_id = transaction.coin_type_id
        self.wallet_repo.check_wallet_balance(wallet=wallet_to, coin_id=coin_id)
        withdrawn_amount = (1 + transaction.commission) * transaction.amount
        if (
            self.wallet_repo.check_wallet_balance(wallet=wallet_from, coin_id=coin_id)
            < withdrawn_amount
        ):
            return None

        self.db.cur.execute(
            """INSERT INTO transactions (amount,
                                         commision,
                                         coin_type_id,
                                         wallet_from_address,
                                         wallet_to_address)
                            VALUES(?,?,?,?,?)""",
            (
                float(transaction.amount),
                float(transaction.commission),
                transaction.coin_type_id,
                transaction.wallet_from_address,
                transaction.wallet_to_address,
            ),
        )
        self.wallet_repo.deposit_to_wallet(
            wallet=wallet_to, coin_id=coin_id, amount=transaction.amount
        )
        self.wallet_repo.withdraw_from_wallet(
            wallet=wallet_from, coin_id=coin_id, amount=withdrawn_amount
        )

        self.db.conn.commit()
        return transaction

    def get_transactions_of_user(self, api_key: str) -> List[TransactionDTO]:
        wallets = self.wallet_repo.get_wallets(api_key=api_key)
        if wallets is None:
            return None
        transactions_list = list(
            map(
                lambda wallet: self._get_transactions(
                    address=wallet.address, address_type=AddressType.to_wallet
                )
                + self._get_transactions(
                    address=wallet.address, address_type=AddressType.from_wallet
                ),
                wallets,
            )
        )
        flat_list = [item for sublist in transactions_list for item in sublist]
        return flat_list

    def get_transactions_sent(self, address: str) -> List[TransactionDTO]:
        return self._get_transaction(
            address=address, address_type=AddressType.to_wallet
        )

    def get_transactions_received(self, address: str) -> List[TransactionDTO]:
        return self._get_transactions(
            address=address, address_type=AddressType.from_wallet
        )

    def _get_transactions(
        self, address: str, address_type: AddressType
    ) -> List[TransactionDTO]:
        try:
            transaction_str = """SELECT amount,
                          commision,
                          coin_type_id,
                          wallet_from_address,
                          wallet_to_address
                     FROM transactions """

            if address_type == AddressType.from_wallet:
                transaction_str += "WHERE wallet_from_address = ?;"
            elif address_type == AddressType.to_wallet:
                transaction_str += "WHERE wallet_to_address = ?;"

            transactions = self.db.cur.execute(
                transaction_str,
                (address,),
            ).fetchall()

            new_transactions = list(
                map(
                    lambda elem: TransactionDTO(
                        amount=Decimal(elem[0]),
                        commission=Decimal(elem[1]),
                        coin_type_id=elem[2],
                        wallet_from_address=elem[3],
                        wallet_to_address=elem[4],
                    ),
                    transactions,
                )
            )
            return new_transactions
        except Exception as e:
            print(e)
            return None
