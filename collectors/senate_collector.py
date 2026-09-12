from bs4 import BeautifulSoup

from collectors.base_paginated_collector import BasePaginatedCollector


class SenateCollector(BasePaginatedCollector):
    """
    Collector for the Senate of Kenya members directory.

    Unlike National Assembly, this page does not require
    JavaScript rendering -- plain HTTP is sufficient.

    Discovers pagination the same way as NationalAssemblyCollector:
    fetch the first page, find the highest page= number in
    pagination links, then build every page URL.
    """

    START_URL = (
        "https://www.parliament.go.ke/"
        "the-senate/senators"
    )

    def __init__(self):
        super().__init__(
            source_name="Senate",
            url=self.START_URL
        )

    def get_page_urls(self):

        html, _, _ = self.download(self.START_URL)

        soup = BeautifulSoup(html, "html.parser")

        page_numbers = set()

        for link in soup.find_all("a", href=True):

            href = link["href"]

            if "page=" not in href:
                continue

            try:
                page_value = (
                    href
                    .split("page=", 1)[1]
                    .split("&", 1)[0]
                )
                page_number = int(page_value)
            except (ValueError, IndexError):
                continue

            page_numbers.add(page_number)

        if not page_numbers:
            raise RuntimeError(
                "Could not discover Senate pagination."
            )

        last_page = max(page_numbers)

        self.logger.info(
            f"Pagination page numbers found: {sorted(page_numbers)}"
        )
        self.logger.info(
            f"Detected last page index: {last_page}"
        )

        urls = []

        for page_number in range(0, last_page + 1):

            if page_number == 0:
                url = self.START_URL
            else:
                url = (
                    f"{self.START_URL}?"
                    f"title="
                    f"&field_parliament_value=2022"
                    f"&page={page_number}"
                )

            urls.append(url)

        self.logger.info(f"Discovered {len(urls)} page(s).")

        return urls

    def collect(self):

        documents = []

        urls = self.get_page_urls()

        total_pages = len(urls)

        for index, url in enumerate(urls, start=1):

            filename = f"senate_{index}.html"

            self.logger.info(
                f"Downloading page {index}/{total_pages} -> {filename}"
            )

            document = self.download_page(
                url=url,
                filename=filename
            )

            documents.append(document)

        self.logger.info(
            f"Senate collection complete: {len(documents)} document(s)."
        )

        return documents


if __name__ == "__main__":

    collector = SenateCollector()
    documents = collector.collect()

    for document in documents:
        print(document.source_url)
