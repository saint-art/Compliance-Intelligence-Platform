from collectors.base_collector import BaseCollector


class CabinetCollector(BaseCollector):
    """
    Collects the official Cabinet page from the
    Presidency website.

    Source:
    https://www.president.go.ke/cabinet/
    """

    def __init__(self):

        super().__init__(

            source_name="Cabinet",

            url="https://www.president.go.ke/cabinet/"

        )