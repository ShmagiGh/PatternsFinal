import sqlite3


class DB:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("Db.sqlite", check_same_thread=False)
        print("Connected")
        self.cur = self.conn.cursor()
