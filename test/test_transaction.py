from app.core.model.transaction_dto import TransactionDTO
from app.core.transaction.transaction_service import TransactionService
from app.infra.in_memory.transaction_memory_repo import InMemoryTransactionRepository

test_transaction_1 = TransactionDTO(
    amount=10.00,
    commission=1,
    coin_type_id=1,
    wallet_from_address="123",
    wallet_to_address="2313",
)


test_transaction_2 = TransactionDTO(
    amount=92.00,
    commission=3,
    coin_type_id=2,
    wallet_from_address="2313",
    wallet_to_address="123",
)


def test_create_transaction() -> None:
    transaction_repo_test = InMemoryTransactionRepository(
        mock_transactions_sent={},
        mock_transactions_received={},
    )
    transactions = TransactionService(transaction_repo=transaction_repo_test)

    assert transactions.create_transaction("123", test_transaction_1) is not None


def test_get_user_transactions() -> None:
    transaction_repo_test = InMemoryTransactionRepository(
        mock_transactions_sent={"123": [test_transaction_1]},
        mock_transactions_received={"2313": [test_transaction_2]},
    )

    transactions = TransactionService(transaction_repo=transaction_repo_test)

    assert transactions.get_transactions_of_user("123")[0].wallet_from_address == "123"
    assert (
        transactions.get_transactions_of_user("2313")[0].wallet_from_address == "2313"
    )


def test_get_sent_transactions() -> None:
    transaction_repo_test = InMemoryTransactionRepository(
        mock_transactions_sent={"123": [test_transaction_1]},
        mock_transactions_received={"2313": [test_transaction_1]},
    )

    transactions = TransactionService(transaction_repo=transaction_repo_test)

    assert transactions.get_transactions_sent("123")[0].wallet_from_address == "123"
    assert transactions.get_transactions_sent("123")[0].wallet_to_address == "2313"


def test_get_received_transactions() -> None:
    transaction_repo_test = InMemoryTransactionRepository(
        mock_transactions_sent={"123": [test_transaction_1]},
        mock_transactions_received={"2313": [test_transaction_1]},
    )

    transactions = TransactionService(transaction_repo=transaction_repo_test)
    assert (
        transactions.get_transactions_received("2313")[0].wallet_from_address == "123"
    )
    assert transactions.get_transactions_received("2313")[0].wallet_to_address == "2313"
