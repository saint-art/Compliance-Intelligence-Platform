from collectors.base_collector import BaseCollector


class KPLCCollector(BaseCollector):
    """
    Collects the Kenya Power (KPLC) Board of Directors page.

    Single page, no pagination, no JavaScript rendering required.
    """

    def __init__(self):
        super().__init__(
            source_name="Kenya Power and Lighting Company",
            url="https://www.kplc.co.ke/board-of-directors"
        )


if __name__ == "__main__":
    collector = KPLCCollector()
    document = collector.collect()
    print(document.to_dict())
