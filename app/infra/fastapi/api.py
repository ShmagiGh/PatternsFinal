import secrets

from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.core import BitcoinWalletCore
from app.core.model.user_dto import UserDTO

user_api = APIRouter()


def get_core(request: Request) -> BitcoinWalletCore:
    core: BitcoinWalletCore = request.app.state.core
    return core


@user_api.post("/users")
def register_user(
        first_name: str, last_name: str, core: BitcoinWalletCore = Depends(get_core)
) -> str:
    api_key = secrets.token_urlsafe(25)
    core.create_user(user=UserDTO(first_name=first_name, last_name=last_name, api_key=api_key))
    return "200 OK"
