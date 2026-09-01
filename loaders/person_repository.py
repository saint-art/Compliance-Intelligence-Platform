from sqlite3 import IntegrityError

from loaders.base_repository import BaseRepository
from models.person import Person
from utils.logger import get_logger


class PersonRepository(BaseRepository):

    def __init__(self, connection=None):
        super().__init__(connection=connection)
        self.logger = get_logger("PersonRepository")

    def person_exists(self, full_name, person: Person):

        self.cursor.execute(
            """
            SELECT person_id
            FROM persons
            WHERE full_name = ?
            AND primary_source = ?
            """,
            (
                full_name,
                person.primary_source
            )
        )

        return self.cursor.fetchone()

    def find_by_name(self, full_name):

        self.cursor.execute(
            """
            SELECT *
            FROM persons
            WHERE full_name = ?
            """,
            (full_name,)
        )

        return self.cursor.fetchone()

    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------

    def save(self, person: Person):

        existing = self.find_by_name(
            person.full_name
        )

        if existing:

            person.person_id = existing["person_id"]

            self.update(person)

            return person.person_id

        return self.insert(person)

    # ---------------------------------------------------------
    # INSERT
    # ---------------------------------------------------------

    def insert(self, person: Person):

        try:

            self.cursor.execute(
                """
                INSERT INTO persons (

                    full_name,
                    first_name,
                    middle_name,
                    last_name,
                    gender,
                    nationality,
                    country,
                    date_of_birth,

                    entity_type,
                    is_pep,
                    is_sanctioned,
                    risk_level,
                    confidence_score,
                    primary_source,
                    last_verified,
                    entity_status,

                    created_at,
                    updated_at,

                    political_party,
                    constituency,
                    county,

                    profile_url,
                    image_url,
                    status

                )

                VALUES (

                    ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?,
                    ?, ?, ?,
                    ?, ?, ?

                )
                """,
                (

                    person.full_name,
                    person.first_name,
                    person.middle_name,
                    person.last_name,
                    person.gender,
                    person.nationality,
                    person.country,
                    person.date_of_birth,

                    person.entity_type,
                    int(person.is_pep),
                    int(person.is_sanctioned),
                    person.risk_level,
                    person.confidence_score,
                    person.primary_source,
                    person.updated_at,
                    person.entity_status,

                    person.created_at,
                    person.updated_at,

                    person.political_party,
                    person.constituency,
                    person.county,

                    person.profile_url,
                    person.image_url,
                    person.status

                )
            )


            person.person_id = self.cursor.lastrowid

            self.logger.info(
                f"Inserted person {person.full_name} "
                f"(ID {person.person_id})"
            )

            return person.person_id

        except IntegrityError:
            raise

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------

    def update(self, person: Person):

        if person.person_id is None:

            raise ValueError(
                "Cannot update Person without person_id."
            )

        self.cursor.execute(
            """
            UPDATE persons

            SET

                full_name = ?,
                first_name = ?,
                middle_name = ?,
                last_name = ?,
                gender = ?,
                nationality = ?,
                country = ?,
                date_of_birth = ?,

                entity_type = ?,
                is_pep = ?,
                is_sanctioned = ?,
                risk_level = ?,
                confidence_score = ?,
                primary_source = ?,
                last_verified = ?,
                entity_status = ?,

                updated_at = ?,

                political_party = ?,
                constituency = ?,
                county = ?,

                profile_url = ?,
                image_url = ?,
                status = ?

            WHERE person_id = ?
            """,
            (

                person.full_name,
                person.first_name,
                person.middle_name,
                person.last_name,
                person.gender,
                person.nationality,
                person.country,
                person.date_of_birth,

                person.entity_type,
                int(person.is_pep),
                int(person.is_sanctioned),
                person.risk_level,
                person.confidence_score,
                person.primary_source,
                person.updated_at,
                person.entity_status,

                person.updated_at,

                person.political_party,
                person.constituency,
                person.county,

                person.profile_url,
                person.image_url,
                person.status,

                person.person_id

            )
        ) 

        self.logger.info(
            f"Updated person {person.full_name} "
            f"(ID {person.person_id})"
        )

        return person.person_id

    # ---------------------------------------------------------
    # BULK
    # ---------------------------------------------------------

    def save_many(self, persons):

        ids = []

        for person in persons:

            ids.append(
                self.save(person)
            )

        return ids