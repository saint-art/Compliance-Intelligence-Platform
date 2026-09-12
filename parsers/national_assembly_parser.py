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


class NationalAssemblyParser(BaseParser):
    """
    Parses one page of the National Assembly MPs directory
    (a Drupal Views table).

    Each page contains up to ~30 MP rows. The full directory
    is 36 pages, each handled as a separate SourceDocument by
    the ingestion pipeline, then merged.

    Table structure (per row):

        td.views-field-field-name          -> full name
        td.views-field-field-image         -> profile link + photo
        td.views-field-field-county        -> county
        td.views-field-field-constituency  -> constituency
        td.views-field-field-party         -> political party
        td.views-field-field-status        -> Elected / Nominated
        td.views-field-view-node           -> "More..." profile link

    Some rows are empty placeholder rows (no name) and must be
    skipped.
    """

    def __init__(self):
        super().__init__("NationalAssemblyParser")

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
            institution_name="National Assembly of Kenya",
            category="Legislature",
            country="Kenya"
        )
        result.institutions.append(institution)

        position = Position(
            title="Member of Parliament",
            category="National Assembly"
        )
        result.positions.append(position)

        # -------------------------------------------------
        # FIND THE MP TABLE
        # -------------------------------------------------

        mp_table = None

        for table in soup.find_all("table"):
            if table.find(
                "td",
                class_="views-field-field-name"
            ):
                mp_table = table
                break

        if mp_table is None:
            self.logger.warning(
                "No MP table found on this page."
            )
            return result

        rows = mp_table.find_all("tr", class_="mp")

        self.logger.info(
            f"Found {len(rows)} candidate rows."
        )

        for row in rows:

            name_cell = row.find(
                "td",
                class_="views-field-field-name"
            )

            full_name = (
                name_cell.get_text(" ", strip=True)
                if name_cell else ""
            )

            # Skip empty placeholder rows.
            if not full_name:
                continue

            county_cell = row.find(
                "td",
                class_="views-field-field-county"
            )
            county = (
                county_cell.get_text(" ", strip=True)
                if county_cell else ""
            )

            constituency_cell = row.find(
                "td",
                class_="views-field-field-constituency"
            )
            constituency = (
                constituency_cell.get_text(" ", strip=True)
                if constituency_cell else ""
            )

            party_cell = row.find(
                "td",
                class_="views-field-field-party"
            )
            party = (
                party_cell.get_text(" ", strip=True)
                if party_cell else ""
            )

            status_cell = row.find(
                "td",
                class_="views-field-field-status"
            )
            status = (
                status_cell.get_text(" ", strip=True)
                if status_cell else ""
            )

            # -------------------------------------------------
            # PROFILE URL + IMAGE
            # (prefer the "More..." link; fall back to the
            #  image cell's link)
            # -------------------------------------------------

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
                    # Skip the generic "photo not available" placeholder.
                    if src and "Photo not available" not in alt:
                        image_url = urljoin(BASE_URL, src)

                if profile_url is None:
                    link = image_cell.find("a", href=True)
                    if link:
                        profile_url = urljoin(
                            BASE_URL,
                            link["href"]
                        )

            # -------------------------------------------------
            # PERSON
            # -------------------------------------------------

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
                constituency=constituency,
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
            f"Extracted {len(result.persons)} MPs from this page."
        )

        return result
