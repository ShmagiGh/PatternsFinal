from decimal import Decimal
from dataclasses import dataclass


@dataclass
class TransactionDTO:
    amount: Decimal
    commission: Decimal
    coin_type_id: int
    wallet_from_address: str
    wallet_to_address: str
