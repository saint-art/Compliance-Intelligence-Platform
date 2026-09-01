from bs4 import BeautifulSoup

from .base_browser_collector import BaseBrowserCollector


class NationalAssemblyCollector(BaseBrowserCollector):

    """
    Browser-based collector for the National Assembly MPs.

    Uses Playwright to render the MPs directory,
    discovers every pagination page,
    downloads each rendered page,
    and returns a list of SourceDocuments.
    """

    START_URL = (
        "https://www.parliament.go.ke/"
        "the-national-assembly/mps"
    )

    def __init__(self):
        super().__init__(
            source_name="National Assembly"
        )

        # -----------------------------------------------------
    # DISCOVER PAGINATION
    # -----------------------------------------------------

    def get_page_urls(self):

        html = self.render_page(
            self.START_URL
        )

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        page_numbers = set()

        # -------------------------------------------------
        # FIND PAGINATION PAGE NUMBERS
        # -------------------------------------------------

        for link in soup.find_all(
            "a",
            href=True
        ):

            href = link["href"]

            if "page=" not in href:
                continue

            try:
                page_value = (
                    href
                    .split("page=", 1)[1]
                    .split("&", 1)[0]
                )

                page_number = int(
                    page_value
                )

            except (
                ValueError,
                IndexError
            ):
                continue

            page_numbers.add(
                page_number
            )

        # -------------------------------------------------
        # DETERMINE LAST PAGE
        # -------------------------------------------------

        if not page_numbers:
            raise RuntimeError(
                "Could not discover National Assembly pagination."
            )

        last_page = max(page_numbers)

        self.logger.info(
            f"Pagination page numbers found: "
            f"{sorted(page_numbers)}"
        )

        self.logger.info(
            f"Detected last page index: {last_page}"
        )

        # -------------------------------------------------
        # BUILD ALL PAGE NUMBERS
        # -------------------------------------------------

        all_page_numbers = range(
            0,
            last_page + 1
        )

        urls = []

        for page_number in all_page_numbers:

            # -------------------------------------------------
            # PAGE 0 = CANONICAL START URL
            # -------------------------------------------------

            if page_number == 0:

                url = self.START_URL

            # -------------------------------------------------
            # OTHER PAGES
            # -------------------------------------------------

            else:

                url = (
                    f"{self.START_URL}?"
                    f"field_name_value=%20"
                    f"&field_parliament_value=2022"
                    f"&field_employment_history_value="
                    f"&page={page_number}"
                )

            urls.append(url)

        # -------------------------------------------------
        # LOG DISCOVERED PAGES
        # -------------------------------------------------

        self.logger.info(
            f"Discovered {len(urls)} page(s)."
        )

        for index, url in enumerate(
            urls,
            start=1
        ):

            self.logger.info(
                f"Page {index}/{len(urls)}: "
                f"{url}"
            )

        return urls

    # -----------------------------------------------------
    # COLLECT
    # -----------------------------------------------------

    def collect(self):

        documents = []

        urls = self.get_page_urls()

        total_pages = len(urls)

        for index, url in enumerate(
            urls,
            start=1
        ):

            filename = (
                f"national_assembly_{index}.html"
            )

            self.logger.info(
                f"Downloading page "
                f"{index}/{total_pages} "
                f"→ {filename}"
            )

            document = self.download_page(
                url=url,
                filename=filename
            )

            documents.append(
                document
            )

        self.logger.info(
            f"National Assembly collection "
            f"complete: {len(documents)} "
            f"document(s)."
        )

        return documents