from urllib.parse import urljoin
from bs4 import BeautifulSoup


class URLDiscovery:
    """
    Discovers relevant pages from an HTML document.
    """

    def __init__(self, base_url: str):

        self.base_url = base_url

        self.allowed_keywords = {

            "administration",
            "cabinet",
            "ministries",
            "office-of-the-president",
            "office-of-the-deputy-president",
            "office-of-the-prime-cabinet-secretary",
            "first-lady"

        }

    def discover(self, html: str):

        soup = BeautifulSoup(html, "lxml")

        urls = set()

        for link in soup.find_all("a", href=True):

            href = link["href"]

            absolute = urljoin(self.base_url, href)

            absolute_lower = absolute.lower()

            if any(
                keyword in absolute_lower
                for keyword in self.allowed_keywords
            ):

                urls.add(absolute)

        return sorted(urls)