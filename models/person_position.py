from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class PersonPosition:

    person_position_id: str = None

    person_id: Optional[int] = None
    position_id: Optional[int] = None
    institution_id: Optional[int] = None

    source_document_id: Optional[str] = None

    start_date: str = ""
    end_date: str = ""

    is_current: bool = True

    confidence_score: float = 100.0

    created_at: str = ""
    updated_at: str = ""

    person: object = None
    position: object = None
    institution: object = None

    def __post_init__(self):

        if self.person_position_id is None:

            self.person_position_id = str(
                uuid.uuid4()
            )

        now = datetime.utcnow().isoformat()

        if not self.created_at:
            self.created_at = now

        if not self.updated_at:
            self.updated_at = now

    def validate(self):

        if self.person_id is None:

            raise ValueError(
                "PersonPosition requires person_id."
            )

        if self.position_id is None:

            raise ValueError(
                "PersonPosition requires position_id."
            )

        if self.institution_id is None:

            raise ValueError(
                "PersonPosition requires institution_id."
            )

        if not self.source_document_id:

            raise ValueError(
                "PersonPosition requires source_document_id."
            )

    def to_dict(self):

        data = asdict(self)

        data.pop("person", None)
        data.pop("position", None)
        data.pop("institution", None)

        return data