from abc import abstractmethod

from collectors.base_collector import BaseCollector


class BasePaginatedCollector(BaseCollector):
    """
    Base class for paginated sources.

    Child collectors only implement get_page_urls().

    This class downloads every page and returns
    a list of SourceDocument objects.
    """

    @abstractmethod
    def get_page_urls(self):
        """
        Return a list of URLs to download.

        Example

        [
            "https://site?page=1",
            "https://site?page=2"
        ]
        """
        pass

    def collect(self):

        documents = []

        urls = self.get_page_urls()

        self.logger.info(
            f"Found {len(urls)} pages."
        )

        for index, url in enumerate(urls, start=1):

            filename = (
                f"{self.source_name.lower().replace(' ', '_')}"
                f"_{index}.html"
            )

            document = self.download_page(
                url=url,
                filename=filename
            )

            documents.append(document)

        return documents