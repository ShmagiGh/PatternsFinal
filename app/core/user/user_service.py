from dataclasses import dataclass
from typing import Protocol

from app.core.model.user_dto import UserDTO
from app.infra.sqlite.user_repo import IUserRepository


class IUser(Protocol):
    def create_user(self, user: UserDTO) -> UserDTO:
        pass


@dataclass
class UserService(IUser):
    _user_repo: IUserRepository

    def create_user(self, user: UserDTO) -> UserDTO:
        return self._user_repo.create_user(user)
