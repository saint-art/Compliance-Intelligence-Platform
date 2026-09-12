"""
Runs every registered source's ingestion pipeline in sequence.

Safe to re-run at any time: every collector/parser/repository in
this platform is idempotent (upsert-by-name, upsert-by-title,
upsert-by-citation), so re-running does not create duplicates.

Note: National Assembly uses Playwright (JS rendering) and will
take several minutes; all other sources use plain HTTP and are
fast.

Run:
    python tools/run_all_pipelines.py
"""

from config.sources import SOURCES
from pipeline.ingestion_pipeline import IngestionPipeline


def main():

    print(f"Running {len(SOURCES)} registered source(s)...\n")

    results = []

    for entry in SOURCES:

        name = entry["name"]
        print(f"{'=' * 60}\n{name}\n{'=' * 60}")

        pipeline = IngestionPipeline(
            collector=entry["collector"](),
            parser=entry["parser"]()
        )

        result = pipeline.run()
        pipeline.close()

        status = "OK" if result.success else "FAILED"
        print(f"[{status}] {name}: {result.entities_saved} entities saved")

        if result.error:
            print(f"  ERROR: {result.error}")

        results.append((name, result.success, result.entities_saved))

    print(f"\n{'=' * 60}\nSUMMARY\n{'=' * 60}")

    for name, success, saved in results:
        marker = "OK  " if success else "FAIL"
        print(f"[{marker}] {name}: {saved}")

    failures = [r for r in results if not r[1]]

    if failures:
        print(f"\n{len(failures)} source(s) failed.")
    else:
        print(f"\nAll {len(results)} source(s) completed successfully.")


if __name__ == "__main__":
    main()
