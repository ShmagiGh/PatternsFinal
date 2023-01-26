from dataclasses import dataclass


@dataclass
class UserDTO:
    first_name: str
    last_name: str
    api_key: str

    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UserDTO):
            return NotImplemented
        return (
            self.first_name == other.first_name
            and self.last_name == other.last_name
            and self.api_key == other.api_key
        )

    def __hash__(self) -> int:
        return hash((self.first_name, self.last_name, self.api_key))
