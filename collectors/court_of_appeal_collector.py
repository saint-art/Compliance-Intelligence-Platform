from collectors.base_collector import BaseCollector


class CourtOfAppealCollector(BaseCollector):
    """
    Collects the Court of Appeal judges page from judiciary.go.ke.

    Single page, no pagination, no JavaScript rendering required.
    """

    def __init__(self):
        super().__init__(
            source_name="Court of Appeal",
            url="https://judiciary.go.ke/court-of-appeal-judges/"
        )


if __name__ == "__main__":
    collector = CourtOfAppealCollector()
    document = collector.collect()
    print(document.to_dict())
