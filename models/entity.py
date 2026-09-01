from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class Entity:
    """
    Base entity for all records in the Compliance Intelligence Platform.
    """

    entity_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    entity_type: str = "ENTITY"

    primary_source: Optional[str] = None

    confidence_score: float = 0.0

    risk_level: str = "LOW"

    entity_status: str = "ACTIVE"

    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    updated_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    def to_dict(self):
        return asdict(self)