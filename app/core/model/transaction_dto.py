from dataclasses import dataclass


@dataclass
class TransactionDTO:
    amount: float
    commission: float
    coin_type_id: int
    wallet_from_address: str
    wallet_to_address: str
