from collectors.presidency_collector import PresidencyCollector
from parsers.presidency_parser import PresidencyParser
from pipeline.ingestion_pipeline import IngestionPipeline

pipeline = IngestionPipeline(
    collector=PresidencyCollector(),
    parser=PresidencyParser()
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
