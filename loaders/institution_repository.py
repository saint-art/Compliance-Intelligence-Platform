from loaders.base_repository import BaseRepository
from models.institution import Institution
from utils.logger import get_logger


class InstitutionRepository(BaseRepository):

    def __init__(self, connection=None):
        super().__init__(connection=connection)

        self.cursor = self.connection.cursor()

        self.logger = get_logger("InstitutionRepository")

    def find_by_name(self, name):

        self.cursor.execute(
            """
            SELECT *
            FROM institutions
            WHERE institution_name=?
            """,
            (name,)
        )

        return self.cursor.fetchone()

    def save(self, institution: Institution):

        existing = self.find_by_name(
            institution.institution_name
        )

        if existing:

            institution.institution_id = existing["institution_id"]

            self.logger.info(
                f"Institution exists: {institution.institution_name}"
            )

            return institution.institution_id

        self.cursor.execute(
            """
            INSERT INTO institutions(

                institution_name,
                category,
                country,
                created_at,
                updated_at

            )

            VALUES(?,?,?,?,?)
            """,
            (
                institution.institution_name,
                institution.category,
                institution.country,
                institution.created_at,
                institution.updated_at
                )
            )
        
        institution.institution_id = self.cursor.lastrowid

        self.logger.info(
                f"Inserted institution {institution.institution_name}"
        )

        return institution.institution_id

    def save_many(self, institutions):

        ids = []

        for institution in institutions:

            ids.append(
                self.save(institution)
            )

        return ids