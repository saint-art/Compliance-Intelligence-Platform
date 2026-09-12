from pathlib import Path

from bs4 import BeautifulSoup

from parsers.base_parser import BaseParser
from parsers.parser_result import ParserResult

from models.person import Person
from models.position import Position
from models.institution import Institution
from models.person_position import PersonPosition


class KRAParser(BaseParser):
    """
    Parses the KRA leadership page.

    Structure (Joomla-based, "cd-trigger" leadership template):

        ul.leadership-list          (one per section: Board / Team)
            a.cd-trigger
                img[src]             -> photo
                span.title           -> full name
                span.designation     -> position title

    Two sections on this page: "KRA Board of Directors" and
    "KRA Leadership Team" -- both captured, tagged with distinct
    categories so board vs. management can be distinguished later.
    """

    def __init__(self):
        super().__init__("KRAParser")

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
            institution_name="Kenya Revenue Authority",
            category="State Corporation",
            country="Kenya"
        )
        result.institutions.append(institution)

        position_cache = {}

        lists = soup.find_all("ul", class_="leadership-list")

        self.logger.info(
            f"Found {len(lists)} leadership-list section(s)."
        )

        for ul in lists:

            heading = ul.find_previous(["h1", "h2", "h3", "h4"])
            section_label = (
                heading.get_text(" ", strip=True)
                if heading else ""
            )

            is_board = "board" in section_label.lower()
            category = "Board" if is_board else "Executive"

            people = ul.find_all("a", class_="cd-trigger")

            self.logger.info(
                f"Section {section_label!r}: {len(people)} people"
            )

            for person_link in people:

                name_span = person_link.find("span", class_="title")
                designation_span = person_link.find(
                    "span", class_="designation"
                )

                full_name = (
                    name_span.get_text(" ", strip=True)
                    if name_span else ""
                )

                if not full_name:
                    continue

                position_title = (
                    designation_span.get_text(" ", strip=True)
                    if designation_span else "Unknown Position"
                )

                image_url = None
                img = person_link.find("img")
                if img:
                    image_url = img.get("src")

                if position_title not in position_cache:
                    position = Position(
                        title=position_title,
                        category=category
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
            f"Extracted {len(result.persons)} KRA leaders."
        )

        return result
