from datetime import datetime

from config.sources import SOURCES


def banner():

    print()

    print("=" * 70)

    print("      COMPLIANCE INTELLIGENCE PLATFORM")

    print("      ETL ORCHESTRATOR")

    print("=" * 70)

    print()


def run():

    start = datetime.now()

    banner()

    total_sources = len(SOURCES)

    print(f"Registered Sources : {total_sources}")

    print()

    for source in SOURCES:

        print("=" * 70)

        print(f"SOURCE : {source['name']}")

        print("=" * 70)

        collector = source["collector"]()

        metadata = collector.collect()

        print("✓ Collection complete")

        parser = source["parser"]()

        parser.parse()

        print("✓ Parsing complete")

        print()

    duration = datetime.now() - start

    print("=" * 70)

    print("PIPELINE COMPLETE")

    print("=" * 70)

    print(f"Processed Sources : {total_sources}")

    print(f"Execution Time    : {duration}")

    print()


if __name__ == "__main__":

    run()