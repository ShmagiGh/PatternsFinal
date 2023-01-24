import sqlite3
from typing import Protocol

from app.core import UserDTO


class IUserRepository(Protocol):
    def create_user(self, user: UserDTO) -> None:
        pass


class UserRepository(IUserRepository):
    def __init__(self) -> None:
        self._database_name = "bitcoin_wallet.db"
        with sqlite3.connect(self._database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    api_key VARCHAR(25) NOT NULL);"""
            )

    def create_user(self, user: UserDTO) -> None:
        with sqlite3.connect(self._database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO users (first_name,last_name,api_key) VALUES(?,?,?)""",
                (user.first_name, user.last_name, user.api_key),
            )
            conn.commit()
