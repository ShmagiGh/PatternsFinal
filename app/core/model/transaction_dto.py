from dataclasses import dataclass, field


@dataclass
class TransactionDTO:
    amount: float
    coin_type_id: int
    api_key: str
    wallet_from_address: str
    wallet_to_address: str
