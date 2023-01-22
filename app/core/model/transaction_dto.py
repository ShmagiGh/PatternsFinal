from dataclasses import dataclass, field


@dataclass
class TransactionDTO:
    amount: float
    commision: float
    coin_type_id: int
    wallet_from_address: str
    wallet_to_address: str
