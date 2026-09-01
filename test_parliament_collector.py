from collectors.national_assembly_collector import NationalAssemblyCollector


def test_national_assembly_collection():
    collector = NationalAssemblyCollector()

    documents = collector.collect()

    assert documents
    assert len(documents) > 0

    for document in documents[:5]:
        print(document.source_url)