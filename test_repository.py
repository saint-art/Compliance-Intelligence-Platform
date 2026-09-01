from models.person import Person
from loaders.person_repository import PersonRepository


def test_person_repository():
    repo = PersonRepository()

    person = Person(
        full_name="Rigathi Gachagua",
        first_name="Rigathi",
        last_name="Gachagua",
        country="Kenya",
        is_pep=True,
        confidence_score=97,
        primary_source="Presidency"
    )

    person_id = repo.save(person)

    assert person_id is not None

    repo.close()