from loaders.base_repository import BaseRepository
from models.position import Position
from utils.logger import get_logger


class PositionRepository(BaseRepository):

    def __init__(self, connection=None):
        super().__init__(connection=connection)
        self.cursor = self.connection.cursor()
        self.logger = get_logger("PositionRepository")

    def find_by_title(self, title):

        self.cursor.execute(
            """
            SELECT *
            FROM positions
            WHERE title = ?
            """,
            (title,)
        )

        return self.cursor.fetchone()

    def save(self, position: Position):

        existing = self.find_by_title(position.title)

        if existing:

            position.position_id = existing["position_id"]

            self.logger.info(
                f"Position exists: {position.title}"
            )

            return position.position_id

        self.cursor.execute(
            """
            INSERT INTO positions(

                title,
                description,
                category,
                created_at,
                updated_at

            )

            VALUES(?,?,?,?,?)
            """,
            (
                position.title,
                position.description,
                position.category,
                position.created_at,
                position.updated_at
            )
        )

        position.position_id = self.cursor.lastrowid

        self.logger.info(
            f"Inserted position {position.title}"
        )

        return position.position_id

    def save_many(self, positions):

        ids = []

        for position in positions:

            ids.append(
                self.save(position)
            )

        return ids