from collectors.presidency_collector import PresidencyCollector
from parsers.presidency_parser import PresidencyParser

from pipeline.ingestion_pipeline import IngestionPipeline


def main():

    pipeline = IngestionPipeline(
        collector=PresidencyCollector(),
        parser=PresidencyParser()
    )

    result = pipeline.run()

    print()
    print("=" * 70)
    print("PIPELINE RESULT")
    print("=" * 70)
    print()
    print(result)


if __name__ == "__main__":
    main()