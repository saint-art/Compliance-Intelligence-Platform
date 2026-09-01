from collectors.national_assembly_collector import NationalAssemblyCollector


def test_browser_collector():
    collector = NationalAssemblyCollector()

    documents = collector.collect()

    assert documents
    assert len(documents) > 0

    for doc in documents:
        print(doc.raw_path)