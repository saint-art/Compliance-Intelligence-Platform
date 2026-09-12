from collectors.base_collector import BaseCollector


class ELRCCollector(BaseCollector):
    """
    Collects the Employment and Labour Relations Court judges
    page from judiciary.go.ke.
    """

    def __init__(self):
        super().__init__(
            source_name="Employment and Labour Relations Court",
            url="https://judiciary.go.ke/employment-and-labour-relations-court-judges/"
        )


if __name__ == "__main__":
    collector = ELRCCollector()
    document = collector.collect()
    print(document.to_dict())
