from typing import Protocol
from app.core.model.transaction_dto import TransactionDTO
from app.infra.sqlite.database import DB
from app.infra.sqlite.transaction_repo import ITransactionRepository


class ITransaction(Protocol):
    def create_transaction(self, transaction: TransactionDTO):
        pass

class TransactionService(ITransaction):
    def __init__(self, db: DB) -> None:
        self._transaction_repo = ITransactionRepository(db)
    def create_transaction(self, transaction: TransactionDTO):
        self._transaction_repo.create_transaction(transaction=transaction)