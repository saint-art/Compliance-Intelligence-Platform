from collectors.presidency_collector import PresidencyCollector
from parsers.presidency_parser import PresidencyParser


def main():

    print("=" * 70)
    print("STEP 1 - Collecting")
    print("=" * 70)

    collector = PresidencyCollector()

    document = collector.collect()

    print("\nSourceDocument created\n")

    for key, value in document.to_dict().items():
        print(f"{key}: {value}")

    print("\n" + "=" * 70)
    print("STEP 2 - Parsing")
    print("=" * 70)

    parser = PresidencyParser()

    persons = parser.parse(document)

    print(f"\nPersons extracted: {len(persons)}")

    print("\n" + "=" * 70)

    for i, person in enumerate(persons, start=1):

        print(f"\nPERSON {i}")
        print("-" * 40)

        for key, value in person.to_dict().items():
            print(f"{key}: {value}")

    print("\nPipeline test completed successfully.")


if __name__ == "__main__":
    main()