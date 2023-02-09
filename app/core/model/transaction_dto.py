from dataclasses import dataclass
from decimal import Decimal


@dataclass
class TransactionDTO:
    amount: Decimal
    commission: Decimal
    coin_type_id: int
    wallet_from_address: str
    wallet_to_address: str
