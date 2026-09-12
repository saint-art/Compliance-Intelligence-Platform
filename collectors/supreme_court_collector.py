from collectors.base_collector import BaseCollector


class SupremeCourtCollector(BaseCollector):
    """
    Collects the Supreme Court judges page from judiciary.go.ke.
    """

    def __init__(self):
        super().__init__(
            source_name="Supreme Court",
            url="https://judiciary.go.ke/supreme-court-judges/"
        )


if __name__ == "__main__":
    collector = SupremeCourtCollector()
    document = collector.collect()
    print(document.to_dict())
