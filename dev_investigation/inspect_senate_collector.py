from collectors.senate_collector import SenateCollector

collector = SenateCollector()
documents = collector.collect()

for document in documents:
    print(document.source_url)
