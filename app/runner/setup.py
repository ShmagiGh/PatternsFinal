from fastapi import FastAPI

from app.core import BitcoinWalletCore
from app.infra.fastapi.transaction_api import transaction_api
from app.infra.fastapi.user_api import user_api
from app.infra.fastapi.wallet_api import wallet_api
from app.infra.sqlite.database import DB
from app.infra.sqlite.user_repo import UserRepository
from app.infra.sqlite.wallet_repo import WalletRepository
from app.infra.sqlite.transaction_repo import TransactionRepository


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(user_api)
    app.include_router(transaction_api)
    app.include_router(wallet_api)
    db = DB()
    user_repository = UserRepository(db)
    wallet_repository = WalletRepository(db)
    transaction_repository = TransactionRepository(db, wallet_repository)
    app.state.core = BitcoinWalletCore.create(user_repository=user_repository,
                                              wallet_repository=wallet_repository,
                                              transaction_repository=transaction_repository)

    return app
