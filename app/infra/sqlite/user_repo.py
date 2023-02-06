from typing import Protocol

from app.core import UserDTO
from app.infra.sqlite.database import DB


class IUserRepository(Protocol):
    def create_user(self, user: UserDTO) -> None:
        pass

    def find_user_by_api_key(self, api_key: str) -> UserDTO:
        pass


class UserRepository(IUserRepository):
    def __init__(self, db: DB) -> None:
        self.db = db
        self.db.cur.execute(
            """CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    api_key VARCHAR(25) NOT NULL);"""
        )

    def create_user(self, user: UserDTO) -> None:
        self.db.cur.execute(
            """INSERT INTO users (first_name,last_name,api_key) VALUES(?,?,?)""",
            (user.first_name, user.last_name, user.api_key),
        )
        self.db.conn.commit()

    def find_user_by_api_key(self, api_key: str) -> UserDTO | None:
        try:
            user = self.db.cur.execute(
                """SELECT u.api_key 
                        FROM users u
                        WHERE u.api_key = ?""",
                api_key).fetchone()[0]
            self.db.conn.commit()
            return user
        except:
            return None
