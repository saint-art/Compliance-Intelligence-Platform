from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Optional


@dataclass
class Source:
    """
    A citation record: which authoritative source document
    supports a given person's PEP status.

    Distinct from SourceDocument (the raw HTML snapshot itself)
    and SourceRun (collector execution audit log). This is the
    compliance-facing citation layer -- what the UN Sanctions
    Explorer or a human reviewer would look at to verify a
    record's provenance.
    """

    source_id: int = None

    person_id: int = None

    source_name: str = ""
    source_url: str = ""
    source_type: str = "HTML"

    trust_score: float = 0.0

    collected_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    last_verified: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    def to_dict(self):
        return asdict(self)
