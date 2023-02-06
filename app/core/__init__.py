from dataclasses import dataclass

from app.core.model.user_dto import UserDTO
from app.core.user.user_service import IUser, IUserRepository, UserService
from app.core.wallet.wallet_service import IWallet, WalletService, RandomAddressGenerator
from app.infra.sqlite.wallet_repo import IWalletRepository


@dataclass
class BitcoinWalletCore:
    userInterface: IUser
    walletInterface: IWallet

    @classmethod
    def create(cls, user_repository: IUserRepository, wallet_repository: IWalletRepository) -> "BitcoinWalletCore":
        return cls(userInterface=UserService(user_repository),
                   walletInterface=WalletService(wallet_repository, RandomAddressGenerator()))
