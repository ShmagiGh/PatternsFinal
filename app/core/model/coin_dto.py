from dataclasses import dataclass, field


@dataclass
class CoinDTO:
    id: int = field(default_factory=int)
    coin: str = field(default_factory=str)
