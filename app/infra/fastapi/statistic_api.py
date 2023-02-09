from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status

from app.core import BitcoinWalletCore
from app.infra.fastapi import get_core

statistic_api = APIRouter(prefix="/statistics", tags=["Statistics"])


ADMIN_KEY = "12345678"


@statistic_api.get("")
def get_profit(
    admin_api_key: str, core: BitcoinWalletCore = Depends(get_core)
) -> Decimal:
    if admin_api_key == ADMIN_KEY:
        return core.statisticInterface.get_commissions_of_all_transactions()

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Admin with this api key is not found",
    )
