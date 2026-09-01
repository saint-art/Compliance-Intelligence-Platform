from collectors.national_assembly_collector import (
    NationalAssemblyCollector
)


def test_national_assembly_pagination():

    collector = NationalAssemblyCollector()

    urls = collector.get_page_urls()

    print("\nDISCOVERED URLS:")
    for index, url in enumerate(urls, start=1):
        print(f"{index:02d}. {url}")

    assert len(urls) == 36

    assert urls[0] == (
        "https://www.parliament.go.ke/"
        "the-national-assembly/mps"
    )

    assert (
        "page=1" in urls[1]
    )

    assert (
        "page=35" in urls[-1]
    )
