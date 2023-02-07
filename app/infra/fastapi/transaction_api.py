from typing import List

from fastapi import APIRouter, HTTPException, status, Depends

from app.core import BitcoinWalletCore
from app.core.model.transaction_dto import TransactionDTO
from app.core.transaction.transaction_service import TransactionService
from app.infra.fastapi import get_core
from app.infra.sqlite.database import DB
from app.infra.sqlite.transaction_repo import TransactionRepository
from app.infra.sqlite.wallet_repo import WalletRepository

transaction_api = APIRouter(prefix="/transactions", tags=["Transactions"])


# db = DB()
# wallet_repo = WalletRepository(db)
# transaction_repo = TransactionRepository(db, wallet_repo)
# transaction_service = transaction_api.transactionInterface

@transaction_api.get("")
def get_user_transactions(api_key: str, core: BitcoinWalletCore = Depends(get_core)) -> List[TransactionDTO]:
    return core.transactionInterface.get_transactions_of_user(api_key)


@transaction_api.post("")
def set_transaction(api_key: str,
                    coin_type_id,
                    from_address: str,
                    to_address: str,
                    amount: str,
                    core: BitcoinWalletCore = Depends(get_core)) -> TransactionDTO:
    commission: float = 0.0
    user_wallets = core.walletInterface.get_wallets(api_key=api_key)
    user_wallets_addresses = map(lambda wallet: wallet.address, user_wallets)

    if from_address not in user_wallets_addresses:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User With this api key has no wallet with that address"
        )

    if not (from_address in user_wallets_addresses and to_address in user_wallets_addresses):
        commission = 1.5  # Constant ებში უნდა გავიტანოთ ან სადმე
    transaction = TransactionDTO(amount=float(amount),
                                 commission=commission,
                                 coin_type_id=coin_type_id,
                                 wallet_from_address=from_address,
                                 wallet_to_address=to_address)
    core.transactionInterface.create_transaction(transaction)
    return transaction
