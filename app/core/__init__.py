from dataclasses import dataclass

from app.core.model.user_dto import UserDTO
from app.core.user.user_service import IUserRepository, UserService, IUser


@dataclass
class BitcoinWalletCore:
    _userInterface: IUser

    @classmethod
    def create(cls, user_repository: IUserRepository) -> "BitcoinWalletCore":
        return cls(
            _userInterface=UserService(user_repository)
        )

    def create_user(self, user: UserDTO) -> None:
        self._userInterface.create_user(user)


