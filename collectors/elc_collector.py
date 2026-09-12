from collectors.base_collector import BaseCollector


class ELCCollector(BaseCollector):
    """
    Collects the Environment and Land Court judges page from
    judiciary.go.ke.
    """

    def __init__(self):
        super().__init__(
            source_name="Environment and Land Court",
            url="https://judiciary.go.ke/environment-and-land-court-judges/"
        )


if __name__ == "__main__":
    collector = ELCCollector()
    document = collector.collect()
    print(document.to_dict())
