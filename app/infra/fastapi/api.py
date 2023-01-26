from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.core import BitcoinWalletCore
from app.core.model.user_dto import UserDTO

user_api = APIRouter()


def get_core(request: Request) -> BitcoinWalletCore:
    core: BitcoinWalletCore = request.app.state.core
    return core


@user_api.post("/users", status_code=201)
def register_user(
        first_name: str, last_name: str, core: BitcoinWalletCore = Depends(get_core)
) -> UserDTO:
    return core.create_user(user=UserDTO(first_name, last_name))
