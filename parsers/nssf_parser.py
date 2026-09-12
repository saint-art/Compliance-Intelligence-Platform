from pathlib import Path

from bs4 import BeautifulSoup

from parsers.base_parser import BaseParser
from parsers.parser_result import ParserResult

from models.person import Person
from models.position import Position
from models.institution import Institution
from models.person_position import PersonPosition


class NSSFParser(BaseParser):
    """
    Parses the NSSF Kenya Board of Trustees page.

    Structure: one small floated single-member table per person,
    each wrapped in div.board_members:

        div.board_members
            table
                tr > td > img[src]      -> photo
                tr > td > div.entry-content > p
                    "<strong>Role</strong> - Name"  (en-dash separator)
    """

    def __init__(self):
        super().__init__("NSSFParser")

    def parse(self, source_document):

        self.logger.info(
            f"Loading {source_document.raw_path}"
        )

        html = Path(
            source_document.raw_path
        ).read_text(
            encoding="utf-8",
            errors="ignore"
        )

        soup = BeautifulSoup(html, "html.parser")

        result = ParserResult(source_document=source_document)

        institution = Institution(
            institution_name="National Social Security Fund",
            category="State Corporation",
            country="Kenya"
        )
        result.institutions.append(institution)

        position_cache = {}

        cards = soup.find_all("div", class_="board_members")

        self.logger.info(
            f"Found {len(cards)} board member card(s)."
        )

        for card in cards:

            p = card.find("p")

            if p is None:
                continue

            text = p.get_text(" ", strip=True)

            if not text or "\u2013" not in text:
                self.logger.warning(
                    f"Unexpected format, skipping: {text!r}"
                )
                continue

            role_part, _, name_part = text.partition("\u2013")

            position_title = role_part.strip()
            full_name = name_part.strip()

            if not full_name:
                continue

            image_url = None
            img = card.find("img")
            if img:
                image_url = img.get("src")

            if position_title not in position_cache:
                position = Position(
                    title=position_title,
                    category="Board"
                )
                position_cache[position_title] = position
                result.positions.append(position)
            else:
                position = position_cache[position_title]

            person = Person(
                full_name=full_name,
                is_pep=True,
                confidence_score=95.0,
                entity_type="PERSON",
                primary_source=source_document.source_name,
                status="ACTIVE",
                nationality="Kenyan",
                country="Kenya",
                image_url=image_url or ""
            )

            result.persons.append(person)

            relationship = PersonPosition(
                confidence_score=95.0,
                is_current=True,
                source_document_id=source_document.document_id,
                person=person,
                position=position,
                institution=institution
            )

            result.relationships.append(relationship)

        self.logger.info(
            f"Extracted {len(result.persons)} NSSF trustees."
        )

        return result
