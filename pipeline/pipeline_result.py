from dataclasses import dataclass
from datetime import datetime


@dataclass
class PipelineResult:

    source_name: str

    documents_processed: int = 0

    entities_created: int = 0

    entities_saved: int = 0

    started_at: str = ""

    finished_at: str = ""

    success: bool = False

    error: str = ""

    def start(self):
        self.started_at = datetime.utcnow().isoformat()

    def finish(self):
        self.finished_at = datetime.utcnow().isoformat()