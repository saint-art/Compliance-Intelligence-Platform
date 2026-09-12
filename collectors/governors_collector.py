from collectors.base_collector import BaseCollector


class GovernorsCollector(BaseCollector):
    """
    Collects the Council of Governors' current governors page.

    Single page, all 47 county governors listed together,
    no pagination, no JavaScript rendering required.
    """

    def __init__(self):
        super().__init__(
            source_name="Governors",
            url="https://cog.go.ke/current-governors/"
        )


if __name__ == "__main__":
    collector = GovernorsCollector()
    document = collector.collect()
    print(document.to_dict())
