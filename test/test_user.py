import pytest

from app.core import IUser, UserService
from app.core.model.user_dto import UserDTO
from app.infra.in_memory.user_memory_repo import InMemoryUserRepository


@pytest.fixture
def service() -> IUser:
    user_repository = InMemoryUserRepository()
    return UserService(user_repository)


def test_create_user(service: IUser) -> None:
    result = service.create_user(
        user=UserDTO(first_name="Dito", last_name="Adeishvili")
    )
    assert result.first_name == "Dito"
    assert result.last_name == "Adeishvili"
    assert result.api_key is not None


def test_create_multiple_user(service: IUser) -> None:
    result = service.create_user(
        user=UserDTO(first_name="Dito", last_name="Adeishvili")
    )
    assert result.first_name == "Dito"
    assert result.last_name == "Adeishvili"
    assert result.api_key is not None
    result = service.create_user(
        user=UserDTO(first_name="Shmagi", last_name="Ghughunishvili")
    )
    assert result.first_name == "Shmagi"
    assert result.last_name == "Ghughunishvili"
    assert result.api_key is not None
    result = service.create_user(
        user=UserDTO(first_name="Bachi", last_name="Skhulukhia")
    )
    assert result.first_name == "Bachi"
    assert result.last_name == "Skhulukhia"
    assert result.api_key is not None


def test_find_user_by_api_key(service: IUser) -> None:
    user = service.create_user(user=UserDTO(first_name="Dito", last_name="Adeishvili"))
    result = service.find_user_by_api_key(user.api_key)
    assert result is not None
    assert result.first_name == "Dito"
    assert result.last_name == "Adeishvili"
    assert result.api_key is not None


def test_find_multiple_user_by_api_key(service: IUser) -> None:
    user = service.create_user(user=UserDTO(first_name="Dito", last_name="Adeishvili"))
    result = service.find_user_by_api_key(user.api_key)
    assert result is not None
    assert result.first_name == "Dito"
    assert result.last_name == "Adeishvili"
    user = service.create_user(
        user=UserDTO(first_name="Shmagi", last_name="Ghughunishvili")
    )
    result = service.find_user_by_api_key(user.api_key)
    assert result.first_name == "Shmagi"
    assert result.last_name == "Ghughunishvili"
    user = service.create_user(user=UserDTO(first_name="Bachi", last_name="Skhulukhia"))
    result = service.find_user_by_api_key(user.api_key)
    assert result.first_name == "Bachi"
    assert result.last_name == "Skhulukhia"
