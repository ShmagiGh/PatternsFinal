from dataclasses import dataclass, field


@dataclass
class WalletDTO:
    api_key: str = field(default_factory=str)
    address: str = field(default_factory=str)
