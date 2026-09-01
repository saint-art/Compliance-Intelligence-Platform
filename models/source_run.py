from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class SourceRun:

    run_id: int = None

    collector_name: str = ""

    source_name: str = ""

    records_found: int = 0

    inserted: int = 0

    updated: int = 0

    skipped: int = 0

    started_at: str = ""

    finished_at: str = ""

    status: str = "RUNNING"

    def __post_init__(self):

        if self.started_at == "":
            self.started_at = datetime.utcnow().isoformat()

    def finish(self):

        self.finished_at = datetime.utcnow().isoformat()

    def to_dict(self):
        return asdict(self)