from collectors.cabinet_collector import CabinetCollector
from parsers.cabinet_parser import CabinetParser
from pipeline.ingestion_pipeline import IngestionPipeline


def test_cabinet_pipeline():
    pipeline = IngestionPipeline(
        CabinetCollector(),
        CabinetParser()
    )

    result = pipeline.run()

    assert result is not None

    print()
    print(result)