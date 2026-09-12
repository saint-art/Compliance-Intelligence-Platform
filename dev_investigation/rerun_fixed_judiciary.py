from collectors.supreme_court_collector import SupremeCourtCollector
from collectors.elrc_collector import ELRCCollector
from parsers.judiciary_parser import JudiciaryParser
from pipeline.ingestion_pipeline import IngestionPipeline

collectors = [
    ("Supreme Court", SupremeCourtCollector),
    ("ELRC", ELRCCollector),
]

for name, collector_class in collectors:
    print(f"\n{'='*60}\n{name}\n{'='*60}")
    pipeline = IngestionPipeline(
        collector=collector_class(),
        parser=JudiciaryParser()
    )
    result = pipeline.run()
    pipeline.close()
    print(f"SUCCESS: {result.success}")
    print(f"ENTITIES SAVED: {result.entities_saved}")
    if result.error:
        print(f"ERROR: {result.error}")
