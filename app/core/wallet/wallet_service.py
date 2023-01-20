from dataclasses import dataclass
from typing import Protocol

from app.core.model.coin import CoinDTO
from app.core.model.wallet_dto import WalletDTO
from app.infra.sqlite.database import DB
from app.infra.sqlite.wallet_repo import IWalletRepository


class IWallet(Protocol):
    def create_wallet(self, wallet: WalletDTO) -> None:
        pass


@dataclass
class WalletService(IWallet):
    def __init__(self, db: DB) -> None:
        self._wallet_repo = IWalletRepository(db)

    def create_wallet(self, wallet: WalletDTO) -> None:
        self._wallet_repo.create_wallet(wallet)

    def deposit_to_wallet(
        self, wallet: WalletDTO, coin: CoinDTO, amount: float
    ) -> None:
        self._wallet_repo.deposit_to_wallet(wallet, coin, amount)

    def withdraw_from_wallet(
        self, wallet: WalletDTO, coin: CoinDTO, amount: float
    ) -> None:
        self._wallet_repo.withdraw_from_wallet(wallet, coin, amount)

    def check_wallet_balance(self, wallet: WalletDTO, coin: CoinDTO) -> float:
        return self._wallet_repo.check_wallet_balance(wallet, coin)
