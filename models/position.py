from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Position:

    position_id: int = None

    title: str = ""

    description: str = ""

    category: str = ""

    created_at: str = ""

    updated_at: str = ""

    def __post_init__(self):

        now = datetime.utcnow().isoformat()

        if self.created_at == "":
            self.created_at = now

        if self.updated_at == "":
            self.updated_at = now

    def to_dict(self):

        return asdict(self)