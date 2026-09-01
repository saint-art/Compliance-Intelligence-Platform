from collectors.cabinet_collector import CabinetCollector


def main():

    collector = CabinetCollector()

    document = collector.collect()

    print()

    print("=" * 60)
    print("CABINET COLLECTOR")
    print("=" * 60)

    print(document.raw_path)
    print(document.source_url)


if __name__ == "__main__":
    main()