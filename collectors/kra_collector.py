from collectors.base_collector import BaseCollector


class KRACollector(BaseCollector):
    """
    Collects the Kenya Revenue Authority leadership page
    (Board of Directors + Leadership Team).

    Single page, no pagination, no JavaScript rendering required.
    """

    def __init__(self):
        super().__init__(
            source_name="Kenya Revenue Authority",
            url="https://www.kra.go.ke/about-kra/leadership"
        )


if __name__ == "__main__":
    collector = KRACollector()
    document = collector.collect()
    print(document.to_dict())
