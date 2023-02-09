import random
import string
from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

from app.core.model.wallet_dto import WalletDTO
from app.infra.sqlite.wallet_repo import IWalletRepository


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
    def create_wallet(self, api_key: str, coin_id: int, amount: Decimal) -> str:
        pass

    def deposit_to_wallet(
        self, wallet: WalletDTO, coin_id: int, amount: Decimal
    ) -> None:
        pass

    def withdraw_from_wallet(
        self, wallet: WalletDTO, coin_id: int, amount: Decimal
    ) -> None:
        pass

    def check_wallet_balance(self, wallet: WalletDTO, coin_id: int) -> Decimal:
        pass

    def check_wallet_count(self, api_key: str) -> int:
        pass

    def get_wallets(self, api_key: str) -> list[WalletDTO]:
        pass


@dataclass
class WalletService(IWallet):
    def __init__(
        self, wallet_repo: IWalletRepository, address_generator: IWalletAddressGenerator
    ) -> None:
        self._wallet_repo = wallet_repo
        self.address_generator = address_generator

    def create_wallet(
        self,
        api_key: str,
        coin_id: int = 1,
        amount: Decimal = Decimal("1"),
    ) -> str:
        address = self.address_generator.generate_address()
        wallet = WalletDTO(api_key=api_key, address=address)
        self._wallet_repo.create_wallet(wallet, coin_id, amount)
        return address

    def deposit_to_wallet(
        self, wallet: WalletDTO, coin_id: int, amount: Decimal
    ) -> None:
        self._wallet_repo.deposit_to_wallet(wallet, coin_id, amount)

    def withdraw_from_wallet(
        self, wallet: WalletDTO, coin_id: int, amount: Decimal
    ) -> None:
        self._wallet_repo.withdraw_from_wallet(wallet, coin_id, amount)

    def check_wallet_balance(self, wallet: WalletDTO, coin_id: int) -> Decimal:
        return self._wallet_repo.check_wallet_balance(wallet, coin_id)

    def check_wallet_count(self, api_key: str) -> int:
        return self._wallet_repo.check_wallet_count(api_key)

    def get_wallets(self, api_key: str) -> list[WalletDTO]:
        return self._wallet_repo.get_wallets(api_key)
