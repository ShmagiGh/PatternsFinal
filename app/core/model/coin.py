from dataclasses import dataclass, field


@dataclass
class CoinDTO:
    coin: str = field(default_factory=str)
    coin_id: int = field(default_factory=int)
