import pytest

from app.core import BitcoinWalletCore
from app.core.model.user_dto import UserDTO
from app.infra.in_memory.user_memory_repo import InMemoryUserRepository


@pytest.fixture
def service() -> BitcoinWalletCore:
    user_repository = InMemoryUserRepository()
    return BitcoinWalletCore.create(user_repository=user_repository)


def test_create_user(service: BitcoinWalletCore) -> None:
    result = service.create_user(user=UserDTO(first_name="Dito", last_name="Adeishvili"))
    assert result.first_name == "Dito"
    assert result.last_name == "Adeishvili"
    assert result.api_key is not None


def test_create_multiple_user(service: BitcoinWalletCore) -> None:
    result = service.create_user(user=UserDTO(first_name="Dito", last_name="Adeishvili"))
    assert result.first_name == "Dito"
    assert result.last_name == "Adeishvili"
    assert result.api_key is not None
    result = service.create_user(user=UserDTO(first_name="Shmagi", last_name="Ghughunishvili"))
    assert result.first_name == "Shmagi"
    assert result.last_name == "Ghughunishvili"
    assert result.api_key is not None
    result = service.create_user(user=UserDTO(first_name="Bachi", last_name="Skhulukhia"))
    assert result.first_name == "Bachi"
    assert result.last_name == "Skhulukhia"
    assert result.api_key is not None
