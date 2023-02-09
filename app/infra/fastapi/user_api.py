from fastapi import APIRouter, Depends

from app.core import BitcoinWalletCore
from app.core.model.user_dto import UserDTO
from app.infra.fastapi import get_core

user_api = APIRouter(prefix="/users", tags=["Users"])


@user_api.post("", status_code=201)
def register_user(
    first_name: str, last_name: str, core: BitcoinWalletCore = Depends(get_core)
) -> UserDTO:
    return core.userInterface.create_user(user=UserDTO(first_name, last_name))
