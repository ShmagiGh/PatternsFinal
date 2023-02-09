from dataclasses import dataclass
from typing import DefaultDict, List

from app.core.model.transaction_dto import TransactionDTO
from app.infra.sqlite.transaction_repo import ITransactionRepository


# api_key and address are the same
@dataclass
class InMemoryTransactionRepository(ITransactionRepository):
    mock_transactions_sent: DefaultDict[str, List[TransactionDTO]]
    mock_transactions_received: DefaultDict[str, List[TransactionDTO]]

    def create_transaction(
        self, api_key: str, transaction: TransactionDTO
    ) -> TransactionDTO | None:
        if transaction.wallet_from_address in self.mock_transactions_sent:
            all_transactions = self.mock_transactions_sent[
                transaction.wallet_from_address
            ]
            all_transactions.append(transaction)
            self.mock_transactions_sent[
                transaction.wallet_from_address
            ] = all_transactions
        else:
            self.mock_transactions_sent[transaction.wallet_from_address] = [transaction]

        if transaction.wallet_to_address in self.mock_transactions_received:
            all_transactions = self.mock_transactions_received[
                transaction.wallet_to_address
            ]
            all_transactions.append(transaction)
            self.mock_transactions_received[
                transaction.wallet_to_address
            ] = all_transactions
        else:
            self.mock_transactions_received[transaction.wallet_to_address] = [
                transaction
            ]
        return transaction

    def get_transactions_of_user(self, api_key: str) -> List[TransactionDTO]:
        all_transactions = list()
        if api_key in self.mock_transactions_sent:
            all_transactions.extend(self.mock_transactions_sent[api_key])
        if api_key in self.mock_transactions_received:
            all_transactions.extend(self.mock_transactions_received[api_key])
        return all_transactions

    def get_transactions_sent(self, address: str) -> List[TransactionDTO]:
        return self.mock_transactions_sent[address]

    def get_transactions_received(self, address: str) -> List[TransactionDTO]:
        return self.mock_transactions_received[address]
