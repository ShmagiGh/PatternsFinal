from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.core import BitcoinWalletCore
from app.core.model.transaction_dto import TransactionDTO
from app.infra.fastapi import get_core

transaction_api = APIRouter(prefix="/transactions", tags=["Transactions"])


# db = DB()
# wallet_repo = WalletRepository(db)
# transaction_repo = TransactionRepository(db, wallet_repo)
# transaction_service = transaction_api.transactionInterface


@transaction_api.get("")
def get_user_transactions(
    api_key: str, core: BitcoinWalletCore = Depends(get_core)
) -> List[TransactionDTO]:
    user_transactions = core.transactionInterface.get_transactions_of_user(api_key)
    if user_transactions is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such user exists."
        )
    return user_transactions


@transaction_api.post("")
def set_transaction(
    api_key: str,
    coin_type_id,
    from_address: str,
    to_address: str,
    amount: str,
    core: BitcoinWalletCore = Depends(get_core),
) -> TransactionDTO:
    commission: Decimal = Decimal(0.0)
    user_wallets = core.walletInterface.get_wallets(api_key=api_key)
    if user_wallets is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such user exists."
        )
    user_wallets_addresses = map(lambda wallet: wallet.address, user_wallets)

    if from_address not in user_wallets_addresses:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User With this api key has no wallet with that address",
        )

    if from_address in user_wallets_addresses and to_address in user_wallets_addresses:
        commission = 0.015  # Constant ებში უნდა გავიტანოთ ან სადმე
    else:
        commission = 0.0
    transaction = TransactionDTO(
        amount=Decimal(amount),
        commission=Decimal(commission),
        coin_type_id=coin_type_id,
        wallet_from_address=from_address,
        wallet_to_address=to_address,
    )
    created = core.transactionInterface.create_transaction(api_key, transaction)
    if created is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Creation Failed"
        )
    return transaction
