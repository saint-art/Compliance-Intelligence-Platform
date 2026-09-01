from collectors.base_collector import BaseCollector


class PresidencyCollector(BaseCollector):

    def __init__(self):

        super().__init__(
            source_name="Presidency",
            url="https://www.president.go.ke/"
        )


if __name__ == "__main__":

    collector = PresidencyCollector()

    document = collector.collect()

    print("\nSOURCE DOCUMENT")
    print("=" * 60)

    for key, value in document.to_dict().items():
        print(f"{key}: {value}")