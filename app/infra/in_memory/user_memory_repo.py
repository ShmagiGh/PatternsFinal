from collections import defaultdict
from typing import DefaultDict

from app.core.model.user_dto import UserDTO
from app.infra.sqlite.user_repo import IUserRepository


class InMemoryUserRepository(IUserRepository):
    _created_users: DefaultDict[UserDTO, int]

    def __init__(self) -> None:
        self._created_users = defaultdict(int)

    def create_user(self, user: UserDTO) -> None:
        self._created_users[user] += 1
