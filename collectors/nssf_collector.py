from collectors.base_collector import BaseCollector


class NSSFCollector(BaseCollector):
    """
    Collects the NSSF Kenya Board of Trustees page.

    Single page, no pagination, no JavaScript rendering required.
    """

    def __init__(self):
        super().__init__(
            source_name="National Social Security Fund",
            url="https://www.nssf.or.ke/board-page"
        )


if __name__ == "__main__":
    collector = NSSFCollector()
    document = collector.collect()
    print(document.to_dict())
