from dataclasses import dataclass, asdict
from datetime import datetime
import uuid


@dataclass
class SourceDocument:

    document_id: str = None

    source_name: str = ""

    source_type: str = ""

    source_url: str = ""

    external_id: str = ""

    title: str = ""

    document_type: str = ""

    published_at: str = ""

    modified_at: str = ""

    collected_at: str = ""

    raw_path: str = ""

    checksum: str = ""

    status: str = "ACTIVE"

    def __post_init__(self):

        if self.document_id is None:
            self.document_id = str(uuid.uuid4())

        if self.collected_at == "":
            self.collected_at = datetime.utcnow().isoformat()

    def to_dict(self):
        return asdict(self)