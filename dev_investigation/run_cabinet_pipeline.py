from collectors.cabinet_collector import CabinetCollector
from parsers.cabinet_parser import CabinetParser
from pipeline.ingestion_pipeline import IngestionPipeline

pipeline = IngestionPipeline(
    collector=CabinetCollector(),
    parser=CabinetParser()
)

result = pipeline.run()
pipeline.close()

print(f"SUCCESS: {result.success}")
print(f"ENTITIES SAVED: {result.entities_saved}")
if result.error:
    print(f"ERROR: {result.error}")
