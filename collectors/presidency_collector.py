from collectors.base_paginated_collector import BasePaginatedCollector


class PresidencyCollector(BasePaginatedCollector):
    """
    Collects the Office of the President page (president.go.ke)
    and the Office of the Deputy President leadership page
    (deputypresident.go.ke).

    Both offices are governed separately with separate official
    domains, so each is treated as its own page within this
    single paginated collector.
    """

    OFFICE_OF_THE_PRESIDENT_URL = (
        "https://www.president.go.ke/administration/office-of-the-president/"
    )

    DEPUTY_PRESIDENT_LEADERSHIP_URL = (
        "https://deputypresident.go.ke/leadership"
    )

    def __init__(self):

        super().__init__(
            source_name="Presidency",
            url=self.OFFICE_OF_THE_PRESIDENT_URL
        )

    def get_page_urls(self):

        return [
            self.OFFICE_OF_THE_PRESIDENT_URL,
            self.DEPUTY_PRESIDENT_LEADERSHIP_URL,
        ]


if __name__ == "__main__":

    collector = PresidencyCollector()

    documents = collector.collect()

    for document in documents:
        print("\nSOURCE DOCUMENT")
        print("=" * 60)
        for key, value in document.to_dict().items():
            print(f"{key}: {value}")
