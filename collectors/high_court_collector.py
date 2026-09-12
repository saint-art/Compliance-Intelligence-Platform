from collectors.base_collector import BaseCollector


class HighCourtCollector(BaseCollector):
    """
    Collects the High Court judges page from judiciary.go.ke.
    """

    def __init__(self):
        super().__init__(
            source_name="High Court",
            url="https://judiciary.go.ke/high-court-judges/"
        )


if __name__ == "__main__":
    collector = HighCourtCollector()
    document = collector.collect()
    print(document.to_dict())
