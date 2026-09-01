from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

from models.entity import Entity


@dataclass
class Person(Entity):

    person_id: int = None

    full_name: str = ""

    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None

    gender: Optional[str] = None
    nationality: Optional[str] = None
    country: Optional[str] = None
    date_of_birth: Optional[str] = None

    is_pep: bool = False
    is_sanctioned: bool = False

    political_party: str = ""
    constituency: str = ""
    county: str = ""

    profile_url: str = ""
    image_url: str = ""

    last_verified: Optional[str] = None

    status: str = ""

    def to_dict(self):
        return asdict(self)