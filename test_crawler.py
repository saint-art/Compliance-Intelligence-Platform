from pathlib import Path

from crawler.url_discovery import URLDiscovery
from crawler.crawler import Crawler


def test_crawler():
    html = Path(
        "input/raw_html/presidency.html"
    ).read_text(encoding="utf-8")

    discovery = URLDiscovery(
        "https://www.president.go.ke"
    )

    urls = discovery.discover(html)

    crawler = Crawler()

    pages = crawler.crawl(urls)

    assert pages

    for page in pages:
        print(page)