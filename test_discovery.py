from pathlib import Path

from crawler.url_discovery import URLDiscovery


def test_url_discovery():
    html = Path(
        "input/raw_html/presidency.html"
    ).read_text(encoding="utf-8")

    discovery = URLDiscovery(
        "https://www.president.go.ke"
    )

    urls = discovery.discover(html)

    assert urls
    assert len(urls) > 0

    for url in urls:
        print(url)