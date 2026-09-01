from pathlib import Path
from urllib.parse import urlparse
from time import perf_counter

import requests

from utils.logger import get_logger


class Crawler:
    """
    Downloads approved pages discovered by URLDiscovery.
    """

    def __init__(self):

        self.logger = get_logger("Crawler")

        self.session = requests.Session()

        self.session.headers.update({

            "User-Agent":
            "Compliance-Intelligence-Platform/1.0"

        })

        self.visited = set()

    def filename_from_url(self, url):

        parsed = urlparse(url)

        path = parsed.path.strip("/")

        if not path:

            return "home.html"

        filename = path.replace("/", "_")

        return f"{filename}.html"

    def crawl(self, urls):

        Path("input/raw_html").mkdir(
            parents=True,
            exist_ok=True
        )

        downloaded = []

        for url in urls:

            if url in self.visited:

                continue

            self.visited.add(url)

            start = perf_counter()

            try:

                response = self.session.get(
                    url,
                    timeout=30
                )

                response.raise_for_status()

                filename = self.filename_from_url(url)

                path = (
                    Path("input/raw_html")
                    / filename
                )

                path.write_text(
                    response.text,
                    encoding="utf-8"
                )

                duration = perf_counter() - start

                self.logger.info(
                    f"{filename} "
                    f"({response.status_code}) "
                    f"{duration:.2f}s"
                )

                downloaded.append({

                    "url": url,
                    "file": str(path),
                    "status": response.status_code

                })

            except Exception as exc:

                self.logger.error(
                    f"{url} -> {exc}"
                )

        return downloaded