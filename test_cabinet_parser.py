from collectors.cabinet_collector import CabinetCollector
from parsers.cabinet_parser import CabinetParser


def test_cabinet_parser():
    collector = CabinetCollector()

    document = collector.collect()

    parser = CabinetParser()

    result = parser.parse(document)

    assert result is not None
    assert len(result.persons) == 24
    assert len(result.positions) == 24
    assert len(result.institutions) == 1
    assert len(result.relationships) == 24

    for person in result.persons[:5]:
        print(person.full_name)