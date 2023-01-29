import random
import string
from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

from app.core.model.coin import CoinDTO
from app.core.model.wallet_dto import WalletDTO
from app.infra.sqlite.database import DB
from app.infra.sqlite.wallet_repo import WalletRepository


class IWalletAddressGenerator(Protocol):
    def generate_address(self) -> str:
        pass


class RandomAddressGenerator(IWalletAddressGenerator):
    def __init__(self):
        self.ADDRESS_LENGTH = 16

    def generate_address(self) -> str:
        return "".join(
            random.choices(
                string.ascii_uppercase + string.ascii_lowercase, k=self.ADDRESS_LENGTH
            )
        )


class IWallet(Protocol):
    def __init__(self, db: DB) -> None:
        pass

    def create_wallet(self, wallet: WalletDTO) -> str:
        pass

    def deposit_to_wallet(
        self, wallet: WalletDTO, coin: CoinDTO, amount: Decimal
    ) -> None:
        pass

    def withdraw_from_wallet(
        self, wallet: WalletDTO, coin: CoinDTO, amount: Decimal
    ) -> None:
        pass

    def check_wallet_balance(self, wallet: WalletDTO, coin: CoinDTO) -> Decimal:
        pass

    def check_wallet_count(self, api_key: str) -> int:
        pass

    def get_wallets(self, api_key: str) -> list[WalletDTO]:
        pass


@dataclass
class WalletService(IWallet):
    def __init__(self, db: DB, address_generator: IWalletAddressGenerator) -> None:
        self._wallet_repo = WalletRepository(db)
        self.address_generator = address_generator

    def create_wallet(
        self,
        api_key: str,
        coin: CoinDTO = CoinDTO("BTC", 1),
        amount: Decimal = Decimal("1"),
    ) -> str:
        address = self.address_generator.generate_address()
        wallet = WalletDTO(api_key=api_key, address=address)
        self._wallet_repo.create_wallet(wallet, coin, amount)
        return address

    def deposit_to_wallet(
        self, wallet: WalletDTO, coin: CoinDTO, amount: Decimal
    ) -> None:
        self._wallet_repo.deposit_to_wallet(wallet, coin, amount)

    def withdraw_from_wallet(
        self, wallet: WalletDTO, coin: CoinDTO, amount: Decimal
    ) -> None:
        self._wallet_repo.withdraw_from_wallet(wallet, coin, amount)

    def check_wallet_balance(self, wallet: WalletDTO, coin: CoinDTO) -> Decimal:
        return self._wallet_repo.check_wallet_balance(wallet, coin)

    def check_wallet_count(self, api_key: str) -> int:
        return self._wallet_repo.check_wallet_count(api_key)

    def get_wallets(self, api_key: str) -> list[WalletDTO]:
        return self._wallet_repo.get_wallets(api_key)
