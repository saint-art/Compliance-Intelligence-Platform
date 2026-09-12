from collectors.nssf_collector import NSSFCollector
from parsers.nssf_parser import NSSFParser
from pipeline.ingestion_pipeline import IngestionPipeline

pipeline = IngestionPipeline(
    collector=NSSFCollector(),
    parser=NSSFParser()
)

result = pipeline.run()
pipeline.close()

print("\n" + "=" * 60)
print(f"SUCCESS: {result.success}")
print(f"ENTITIES SAVED: {result.entities_saved}")
if result.error:
    print(f"ERROR: {result.error}")
