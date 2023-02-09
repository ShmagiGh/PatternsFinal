import sqlite3
from decimal import Decimal

from app.core.model.coin_dto import CoinDTO
from app.core.model.user_dto import UserDTO
from app.core.model.wallet_dto import WalletDTO
from app.core.wallet.wallet_service import RandomAddressGenerator, WalletService
from app.infra.sqlite.wallet_repo import WalletRepository


class TestDB:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("TestDb.sqlite", check_same_thread=False)
        print("Connected")
        self.cur = self.conn.cursor()


db = TestDB()
db.cur.execute(
    """
                DROP table if exists wallets;
                """
)
db.cur.execute(
    """
                DROP table if exists balances;
                """
)
wallet_repo = WalletRepository(db)
wallet_service = WalletService(wallet_repo, RandomAddressGenerator())

coin_btc = CoinDTO(1, "BTC")
coin_satoshi = CoinDTO(2, "SATOSHI")

user1 = UserDTO("a2", "a3")
user2 = UserDTO("b2", "b3")
user3 = UserDTO("c2", "c3")

user1_api_key = "a1"
user2_api_key = "a2"
user3_api_key = "a3"

addresses = {}

wallets = {}


def test_create_wallet():
    addresses["address1"] = wallet_service.create_wallet(user1_api_key)
    wallets["wallet1"] = WalletDTO(user1_api_key, addresses["address1"])
    assert type(addresses["address1"]) == str
    assert len(addresses["address1"]) == 16


def test_deposit_wallet():
    wallet_service.deposit_to_wallet(wallets["wallet1"], coin_btc.id, Decimal("1.4"))
    wallet_service.deposit_to_wallet(wallets["wallet1"], coin_btc.id, Decimal("2.2"))
    assert wallet_service.check_wallet_balance(
        wallets["wallet1"], coin_btc.id
    ) == Decimal("4.6")


def test_withdraw_wallet():
    wallet_service.withdraw_from_wallet(wallets["wallet1"], coin_btc.id, Decimal("0.7"))
    assert wallet_service.check_wallet_balance(
        wallets["wallet1"], coin_btc.id
    ) == Decimal("3.9")


def test_wallet_count():
    addresses["address2"] = wallet_service.create_wallet(user2_api_key)
    wallets["wallet2"] = WalletDTO(user2_api_key, addresses["address2"])

    addresses["address3"] = wallet_service.create_wallet(user2_api_key)
    wallets["wallet3"] = WalletDTO(user2_api_key, addresses["address3"])

    addresses["address4"] = wallet_service.create_wallet(user2_api_key)
    wallets["wallet4"] = WalletDTO(user2_api_key, addresses["address4"])

    assert wallet_service.check_wallet_count(user1_api_key) == 1
    assert wallet_service.check_wallet_count(user2_api_key) == 3
    assert wallet_service.check_wallet_count(user3_api_key) == 0


def test_get_wallet():
    assert wallet_service.get_wallets("a1") == [wallets["wallet1"]]
    assert wallet_service.get_wallets("a2") == [
        wallets["wallet2"],
        wallets["wallet3"],
        wallets["wallet4"],
    ]
    assert wallet_service.get_wallets("a3") == []
