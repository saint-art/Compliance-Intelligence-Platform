from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from parsers.base_parser import BaseParser
from parsers.parser_result import ParserResult

from models.person import Person
from models.position import Position
from models.institution import Institution
from models.person_position import PersonPosition


BASE_URL = "https://www.parliament.go.ke"


class SenateParser(BaseParser):
    """
    Parses one page of the Senate of Kenya members directory
    (a Drupal Views table).

    Table structure (per row):

        td.views-field-field-senator          -> full name
        td.views-field-field-image            -> photo
        td.views-field-field-county-senator    -> county
        td.views-field-field-party-senator     -> political party
        td.views-field-field-status-senator    -> Elected / Nominated
        td.views-field-view-node               -> "More Info" profile link
    """

    def __init__(self):
        super().__init__("SenateParser")

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
            institution_name="Senate of Kenya",
            category="Legislature",
            country="Kenya"
        )
        result.institutions.append(institution)

        position = Position(
            title="Senator",
            category="Senate"
        )
        result.positions.append(position)

        senator_table = None

        for table in soup.find_all("table"):
            if table.find(
                "td",
                class_="views-field-field-senator"
            ):
                senator_table = table
                break

        if senator_table is None:
            self.logger.warning(
                "No senator table found on this page."
            )
            return result

        rows = senator_table.find_all("tr")

        self.logger.info(
            f"Found {len(rows)} candidate rows."
        )

        for row in rows:

            name_cell = row.find(
                "td",
                class_="views-field-field-senator"
            )

            full_name = (
                name_cell.get_text(" ", strip=True)
                if name_cell else ""
            )

            if not full_name:
                continue

            county_cell = row.find(
                "td",
                class_="views-field-field-county-senator"
            )
            county = (
                county_cell.get_text(" ", strip=True)
                if county_cell else ""
            )

            party_cell = row.find(
                "td",
                class_="views-field-field-party-senator"
            )
            party = (
                party_cell.get_text(" ", strip=True)
                if party_cell else ""
            )

            profile_url = None

            view_node_cell = row.find(
                "td",
                class_="views-field-view-node"
            )
            if view_node_cell:
                link = view_node_cell.find("a", href=True)
                if link:
                    profile_url = urljoin(
                        BASE_URL,
                        link["href"]
                    )

            image_url = None

            image_cell = row.find(
                "td",
                class_="views-field-field-image"
            )
            if image_cell:
                img = image_cell.find("img")
                if img:
                    src = img.get("src")
                    alt = img.get("alt", "")
                    if src and "Photo not available" not in alt:
                        image_url = urljoin(BASE_URL, src)

            # "Nominated" senators have county="Nominated" rather
            # than a real county name -- preserve as-is since it's
            # what the source says, not an extraction error.

            person = Person(
                full_name=full_name,
                is_pep=True,
                confidence_score=95.0,
                entity_type="PERSON",
                primary_source=source_document.source_name,
                status="ACTIVE",
                nationality="Kenyan",
                country="Kenya",
                political_party=party,
                county=county,
                profile_url=profile_url or "",
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
            f"Extracted {len(result.persons)} senators from this page."
        )

        return result
