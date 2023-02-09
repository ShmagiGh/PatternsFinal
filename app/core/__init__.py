from dataclasses import dataclass

from app.core.coin.coin_service import ICoin, CoinService
from app.core.model.user_dto import UserDTO
from app.core.transaction.transaction_service import ITransaction, TransactionService
from app.core.user.user_service import IUser, IUserRepository, UserService
from app.core.wallet.wallet_service import IWallet, WalletService, RandomAddressGenerator
from app.infra.sqlite.coin_repo import ICoinRepository
from app.infra.sqlite.transaction_repo import ITransactionRepository
from app.infra.sqlite.wallet_repo import IWalletRepository


@dataclass
class BitcoinWalletCore:
    userInterface: IUser
    walletInterface: IWallet
    transactionInterface: ITransaction
    coinInterface: ICoin

    @classmethod
    def create(cls,
               user_repository: IUserRepository,
               wallet_repository: IWalletRepository,
               transaction_repository: ITransactionRepository,
               coin_repository: ICoinRepository) -> "BitcoinWalletCore":
        return cls(userInterface=UserService(user_repository),
                   walletInterface=WalletService(wallet_repository, RandomAddressGenerator()),
                   transactionInterface=TransactionService(transaction_repository),
                   coinInterface=CoinService(coin_repository))
