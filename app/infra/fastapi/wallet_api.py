from fastapi import APIRouter, Path, HTTPException, status, Depends

from app.core import BitcoinWalletCore
from app.core.model.coin import CoinDTO
from app.core.model.wallet_dto import WalletDTO
from app.infra.fastapi import get_core


wallet_api = APIRouter()


@wallet_api.post("/wallets")
def post_wallet(api_key: str, core: BitcoinWalletCore = Depends(get_core)):
    if core.userInterface.find_user_by_api_key(api_key) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such user exists."
        )

    wallet_count = core.walletInterface.check_wallet_count(api_key)
    if wallet_count >= 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User can't have more than 3 wallets."
        )
    address = core.walletInterface.create_wallet(api_key=api_key)
    return address, CoinDTO("BTC", 1)


@wallet_api.get("/wallet/{address}")
def get_wallet(
        api_key: str,
        address: str = Path(None, description="This is address of wallet"),
        core: BitcoinWalletCore = Depends(get_core)
):
    balance_btc = core.walletInterface.check_wallet_balance(WalletDTO(api_key, address), CoinDTO("BTC", 1))
    if balance_btc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such wallet exists."
        )
    return address, balance_btc
