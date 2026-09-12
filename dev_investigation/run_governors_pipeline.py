from collectors.governors_collector import GovernorsCollector
from parsers.governors_parser import GovernorsParser
from pipeline.ingestion_pipeline import IngestionPipeline

pipeline = IngestionPipeline(
    collector=GovernorsCollector(),
    parser=GovernorsParser()
)

result = pipeline.run()
pipeline.close()

print("\n" + "=" * 60)
print(f"SUCCESS: {result.success}")
print(f"ENTITIES SAVED: {result.entities_saved}")
if result.error:
    print(f"ERROR: {result.error}")
