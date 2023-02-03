from fastapi import FastAPI

from app.core import BitcoinWalletCore
from app.infra.fastapi.api import user_api
from app.infra.fastapi.transaction_api import transaction_api
from app.infra.sqlite.user_repo import UserRepository


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(user_api)
    app.include_router(transaction_api)
    user_repository = UserRepository()
    app.state.core = BitcoinWalletCore.create(user_repository=user_repository)

    return app
