from dataclasses import dataclass


@dataclass
class UserDTO:
    first_name: str
    last_name: str
    api_key: str
