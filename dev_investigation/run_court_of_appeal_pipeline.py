from collectors.court_of_appeal_collector import CourtOfAppealCollector
from parsers.judiciary_parser import JudiciaryParser
from pipeline.ingestion_pipeline import IngestionPipeline

pipeline = IngestionPipeline(
    collector=CourtOfAppealCollector(),
    parser=JudiciaryParser()
)

result = pipeline.run()
pipeline.close()

print("\n" + "=" * 60)
print(f"SUCCESS: {result.success}")
print(f"ENTITIES SAVED: {result.entities_saved}")
if result.error:
    print(f"ERROR: {result.error}")
