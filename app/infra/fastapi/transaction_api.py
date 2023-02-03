from typing import List

from fastapi import APIRouter

from app.core.model.transaction_dto import TransactionDTO

transaction_api = APIRouter(prefix="/transactions", tags=["Transactions"])

# TODO: შესავსებია პოსტ/გეთ მეთოდები


@transaction_api.get("")
def get_user_transactions(api_key: str) -> List[TransactionDTO]:
    return []


@transaction_api.post("")
def set_transaction(api_key: str) -> List[TransactionDTO]:
    return []
