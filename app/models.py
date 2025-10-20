from dataclasses import dataclass, field
from datetime import date


@dataclass
class User:
    id: int
    full_name: str
    email: str
    doc_number: str
    username: str
    password: str
    logged_in: bool = False
    created_at: date = field(default_factory=date.today)
    updated_at: date = field(default_factory=date.today)


@dataclass
class Token:
    id_user: int
    token: str
    created_at: date = field(default_factory=date.today)
