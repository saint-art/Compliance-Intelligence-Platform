from collectors.senate_collector import SenateCollector
from parsers.senate_parser import SenateParser
from pipeline.ingestion_pipeline import IngestionPipeline

pipeline = IngestionPipeline(
    collector=SenateCollector(),
    parser=SenateParser()
)

result = pipeline.run()
pipeline.close()

print("\n" + "=" * 60)
print(f"SUCCESS: {result.success}")
print(f"DOCUMENTS PROCESSED: {result.documents_processed}")
print(f"ENTITIES CREATED: {result.entities_created}")
print(f"ENTITIES SAVED: {result.entities_saved}")
if result.error:
    print(f"ERROR: {result.error}")
