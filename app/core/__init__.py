from dataclasses import dataclass

from app.core.model.user_dto import UserDTO
from app.core.user.user_service import IUser, IUserRepository, UserService


@dataclass
class BitcoinWalletCore:
    _userInterface: IUser

    @classmethod
    def create(cls, user_repository: IUserRepository) -> "BitcoinWalletCore":
        return cls(_userInterface=UserService(user_repository))

    def create_user(self, user: UserDTO) -> UserDTO:
        return self._userInterface.create_user(user)

    def find_user_by_api_key(self, api_key: str) -> UserDTO:
        return self._userInterface.find_user_by_api_key(api_key)
