from fastapi import FastAPI

from app.core import BitcoinWalletCore
from app.infra.fastapi.statistic_api import statistic_api
from app.infra.fastapi.transaction_api import transaction_api
from app.infra.fastapi.user_api import user_api
from app.infra.fastapi.wallet_api import wallet_api
from app.infra.sqlite.coin_repo import CoinRepository
from app.infra.sqlite.database import DB
from app.infra.sqlite.statistic_repo import StatisticRepository
from app.infra.sqlite.transaction_repo import TransactionRepository
from app.infra.sqlite.user_repo import UserRepository
from app.infra.sqlite.wallet_repo import WalletRepository


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(user_api)
    app.include_router(transaction_api)
    app.include_router(wallet_api)
    app.include_router(statistic_api)
    db = DB()
    user_repository = UserRepository(db)
    wallet_repository = WalletRepository(db)
    coin_repository = CoinRepository(db)
    transaction_repository = TransactionRepository(db, wallet_repository)
    statistic_repository = StatisticRepository(db)
    app.state.core = BitcoinWalletCore.create(
        user_repository=user_repository,
        wallet_repository=wallet_repository,
        transaction_repository=transaction_repository,
        coin_repository=coin_repository,
        statistic_repository=statistic_repository,
    )

    return app
