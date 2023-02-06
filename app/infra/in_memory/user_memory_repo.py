from collections import defaultdict
from typing import DefaultDict

from app.core.model.user_dto import UserDTO
from app.infra.sqlite.user_repo import IUserRepository


class InMemoryUserRepository(IUserRepository):
    _created_users: DefaultDict[str, UserDTO]

    def __init__(self) -> None:
        self._created_users = defaultdict()

    def create_user(self, user: UserDTO) -> None:
        self._created_users[user.api_key] = user

    def find_user_by_api_key(self, api_key: str) -> UserDTO:
        return self._created_users[api_key]
