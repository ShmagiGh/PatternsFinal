from fastapi import APIRouter, Path, HTTPException, status, FastAPI
from app.infra.sqlite.database import DB
from app.core.wallet.wallet_service import WalletService, RandomAddressGenerator
from app.core.model.coin import CoinDTO
from app.core.model.wallet_dto import WalletDTO
from decimal import Decimal

db = DB()
wallet_service = WalletService(db, RandomAddressGenerator())
wallet_api = FastAPI()


@wallet_api.post("/wallets")
def post_wallet(api_key: str):
    wallet_count = wallet_service.check_wallet_count(api_key)
    if wallet_count >= 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User can't have more than 3 wallets."
        )
    address = wallet_service.create_wallet(api_key=api_key, coin=CoinDTO("BTC", 1), amount=Decimal("1"))
    return address, CoinDTO("BTC", 1)


@wallet_api.get("/wallet/{address}")
def get_wallet(api_key: str, address: str = Path(None, description="This is address of wallet")):
    balance_btc = wallet_service.check_wallet_balance(WalletDTO(api_key, address), CoinDTO("BTC", 1))
    if balance_btc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such wallet exists."
        )
    return address, balance_btc
