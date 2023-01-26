import sqlite3


class TestDB:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("TestDb.sqlite", check_same_thread=False)
        print("Connected")
        self.cur = self.conn.cursor()
