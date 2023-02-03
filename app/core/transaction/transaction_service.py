from dataclasses import dataclass
from typing import List, Protocol

from app.core.model.transaction_dto import TransactionDTO
from app.infra.sqlite.transaction_repo import ITransactionRepository


class ITransaction(Protocol):
    def create_transaction(self, transaction: TransactionDTO) -> None:
        pass

    def get_transactions_of_user(self, api_key: str) -> List[TransactionDTO]:
        pass

    def get_transactions_sent(self, address: str) -> List[TransactionDTO]:
        pass

    def get_transactions_received(self, address: str) -> List[TransactionDTO]:
        pass


@dataclass
class TransactionService(ITransaction):
    transaction_repo: ITransactionRepository

    def create_transaction(self, transaction: TransactionDTO) -> None:
        self.transaction_repo.create_transaction(transaction=transaction)

    def get_transactions_of_user(self, api_key: str) -> List[TransactionDTO]:
        return self.transaction_repo.get_transactions_of_user(api_key=api_key)

    def get_transactions_sent(self, address: str) -> List[TransactionDTO]:
        return self.transaction_repo.get_transactions_sent(address=address)

    def get_transactions_received(self, address: str) -> List[TransactionDTO]:
        return self.transaction_repo.get_transactions_received(address=address)
