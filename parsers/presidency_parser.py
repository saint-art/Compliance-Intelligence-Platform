from pathlib import Path

from bs4 import BeautifulSoup

from parsers.base_parser import BaseParser
from parsers.parser_result import ParserResult

from models.person import Person
from models.position import Position
from models.institution import Institution
from models.person_position import PersonPosition


class PresidencyParser(BaseParser):
    """
    Parses two distinct official sources:

    1. Office of the President (president.go.ke)
       - The President
       - Chief of Staff / Head of Public Service
       - State House Comptroller

    2. Office of the Deputy President (deputypresident.go.ke)
       - The Deputy President
       - Chief of Staff (ODP)
       - Principal Secretaries / Principal Administrative Secretary

    Each source has a different page structure, so parse()
    dispatches to a dedicated method based on source_url.
    """

    def __init__(self):
        super().__init__("PresidencyParser")

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

        soup = BeautifulSoup(html, "lxml")

        if "deputypresident.go.ke" in source_document.source_url:
            result = self._parse_deputy_president(soup, source_document)
        else:
            result = self._parse_office_of_the_president(soup, source_document)

        self.logger.info(
            f"Extracted "
            f"{len(result.persons)} persons, "
            f"{len(result.positions)} positions, "
            f"{len(result.institutions)} institutions, "
            f"{len(result.relationships)} relationships."
        )

        return result

    # -----------------------------------------------------------
    # OFFICE OF THE PRESIDENT
    # -----------------------------------------------------------

    def _parse_office_of_the_president(self, soup, source_document):

        result = ParserResult(source_document=source_document)

        institution = Institution(
            institution_name="Office of the President",
            category="Executive",
            country="Kenya"
        )
        result.institutions.append(institution)

        # -------------------------------------------------
        # THE PRESIDENT
        # (name + title concatenated in one heading)
        # -------------------------------------------------

        president_heading = None
        for h in soup.find_all("h4", class_="brxe-heading"):
            classes = h.get("class", [])
            if "brxe-xplzry" not in classes:
                text = h.get_text(" ", strip=True)
                if "President" in text:
                    president_heading = text
                    break

        if president_heading:

            marker = "President of the Republic of Kenya"
            idx = president_heading.find(marker)

            if idx != -1:
                name = president_heading[:idx].rstrip(", ").strip()
                title = president_heading[idx:].strip().rstrip(".")
            else:
                name = president_heading
                title = "President of the Republic of Kenya"

            self._add_person(
                result, source_document, institution,
                full_name=name,
                position_title=title,
                confidence_score=99.0
            )
        else:
            self.logger.warning(
                "Could not locate President heading on "
                "Office of the President page."
            )

        # -------------------------------------------------
        # OTHER OFFICE HOLDERS
        # (name in h4.brxe-xplzry.brxe-heading,
        #  title in sibling div.brxe-cqgolm.brxe-text-basic)
        # -------------------------------------------------

        for heading in soup.select("h4.brxe-xplzry.brxe-heading"):

            name = heading.get_text(" ", strip=True)
            if not name:
                continue

            parent = heading.parent
            title_div = parent.find("div", class_="brxe-cqgolm") if parent else None
            title = title_div.get_text(" ", strip=True) if title_div else "Unknown Position - Office of the President"

            self._add_person(
                result, source_document, institution,
                full_name=name,
                position_title=title,
                confidence_score=97.0
            )

        return result

    # -----------------------------------------------------------
    # OFFICE OF THE DEPUTY PRESIDENT
    # -----------------------------------------------------------

    def _parse_deputy_president(self, soup, source_document):

        result = ParserResult(source_document=source_document)

        institution = Institution(
            institution_name="Office of the Deputy President",
            category="Executive",
            country="Kenya"
        )
        result.institutions.append(institution)

        cards = soup.find_all("div", class_="gsc-column")

        for card in cards:

            desc = card.find("div", class_="desc")

            if desc is None:
                continue

            full_text = desc.get_text(" ", strip=True)

            if not full_text:
                continue

            strong = desc.find("strong")

            if strong is None:
                continue

            name = strong.get_text(" ", strip=True)

            if not name:
                continue

            title = full_text.replace(name, "", 1).strip(" ,")

            if not title:
                title = "Unknown Position - Office of the Deputy President"

            is_dp = title.strip().lower().startswith("the deputy president")

            self._add_person(
                result, source_document, institution,
                full_name=name,
                position_title=title,
                confidence_score=99.0 if is_dp else 95.0
            )

        return result

    # -----------------------------------------------------------
    # SHARED HELPER
    # -----------------------------------------------------------

    def _add_person(
        self,
        result,
        source_document,
        institution,
        full_name,
        position_title,
        confidence_score
    ):

        person = Person(
            full_name=full_name,
            is_pep=True,
            confidence_score=confidence_score,
            entity_type="PERSON",
            primary_source=source_document.source_name,
            status="ACTIVE",
            nationality="Kenyan",
            country="Kenya"
        )

        position = Position(
            title=position_title,
            category="Presidency"
        )

        result.persons.append(person)
        result.positions.append(position)

        relationship = PersonPosition(
            confidence_score=confidence_score,
            is_current=True,
            source_document_id=source_document.document_id,
            person=person,
            position=position,
            institution=institution
        )

        result.relationships.append(relationship)
