from pathlib import Path

from bs4 import BeautifulSoup

from parsers.base_parser import BaseParser
from parsers.parser_result import ParserResult

from models.person import Person
from models.position import Position
from models.institution import Institution
from models.person_position import PersonPosition


class GovernorsParser(BaseParser):
    """
    Parses the Council of Governors' current governors page.

    Card structure (repeated 47 times):

        div.leader-card
            div.leader-thumbnail
                img[src]      -> photo (already an absolute URL)
            div.captions
                h3            -> full name
                p              -> "County: <name>"

    No profile link is present on this page.
    """

    def __init__(self):
        super().__init__("GovernorsParser")

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
            institution_name="Council of Governors of Kenya",
            category="County Government",
            country="Kenya"
        )
        result.institutions.append(institution)

        position = Position(
            title="Governor",
            category="County Government"
        )
        result.positions.append(position)

        cards = soup.find_all("div", class_="leader-card")

        self.logger.info(
            f"Found {len(cards)} governor card(s)."
        )

        for card in cards:

            heading = card.find("h3")

            full_name = (
                heading.get_text(" ", strip=True)
                if heading else ""
            )

            if not full_name:
                continue

            captions = card.find("div", class_="captions")

            county = ""

            if captions:
                county_p = captions.find("p")
                if county_p:
                    text = county_p.get_text(" ", strip=True)
                    if ":" in text:
                        county = text.split(":", 1)[1].strip()
                    else:
                        county = text.strip()

            image_url = None

            thumb = card.find("div", class_="leader-thumbnail")
            if thumb:
                img = thumb.find("img")
                if img:
                    image_url = img.get("src")

            person = Person(
                full_name=full_name,
                is_pep=True,
                confidence_score=97.0,
                entity_type="PERSON",
                primary_source=source_document.source_name,
                status="ACTIVE",
                nationality="Kenyan",
                country="Kenya",
                county=county,
                image_url=image_url or ""
            )

            result.persons.append(person)

            relationship = PersonPosition(
                confidence_score=97.0,
                is_current=True,
                source_document_id=source_document.document_id,
                person=person,
                position=position,
                institution=institution
            )

            result.relationships.append(relationship)

        self.logger.info(
            f"Extracted {len(result.persons)} governors."
        )

        return result
