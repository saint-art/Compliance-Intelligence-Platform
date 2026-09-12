from pathlib import Path

from bs4 import BeautifulSoup

from parsers.base_parser import BaseParser
from parsers.parser_result import ParserResult

from models.person import Person
from models.position import Position
from models.institution import Institution
from models.person_position import PersonPosition


# Maps every known surface form (full names AND abbreviations)
# to a single canonical court name. Sorted by length (longest
# first) at match time so full names are preferred over any
# abbreviation that might also appear as a substring.
COURT_ALIASES = {
    "Supreme Court": "Supreme Court",
    "Court of Appeal": "Court of Appeal",
    "Employment and Labour Relations Court": "Employment and Labour Relations Court",
    "ELRC": "Employment and Labour Relations Court",
    "Environment and Land Court": "Environment and Land Court",
    "ELC": "Environment and Land Court",
    "High Court": "High Court",
}

# Connector words/punctuation that can trail the title portion
# once the court name itself has been located and removed.
# Checked longest-first so "of the" is stripped before "of".
TRAILING_CONNECTORS = [" of the", " of", ","]


class JudiciaryParser(BaseParser):
    """
    Generic parser for judiciary.go.ke's judges pages.

    Works across all court levels (Supreme Court, Court of
    Appeal, High Court, ELRC, ELC) because they all share the
    same WordPress team-member plugin markup:

        div.wpb-team-default-item
            div.person_image
                img[src]              -> photo
            div.person-info
                h5.wpb-otm-name > a   -> full name + profile URL
                span.designation      -> title + court, in one
                                          of several formats:
                                          "Judge, Court of Appeal"
                                          "Judge of the Supreme Court of Kenya"
                                          "judge of the ELRC"
                div.wpb-otm-bio       -> biography (not extracted)

    _split_designation() normalizes all of these into
    (title, canonical_court_name).
    """

    def __init__(self):
        super().__init__("JudiciaryParser")

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

        institution_cache = {}
        position_cache = {}

        cards = soup.find_all(
            "div",
            class_="wpb-team-default-item"
        )

        self.logger.info(
            f"Found {len(cards)} judge card(s)."
        )

        for card in cards:

            name_heading = card.find("h5", class_="wpb-otm-name")

            if name_heading is None:
                continue

            name_link = name_heading.find("a")

            full_name = (
                name_link.get_text(" ", strip=True)
                if name_link else
                name_heading.get_text(" ", strip=True)
            )

            if not full_name:
                continue

            profile_url = (
                name_link.get("href") if name_link else ""
            )

            designation_span = card.find(
                "span",
                class_="designation"
            )

            designation = (
                designation_span.get_text(" ", strip=True)
                if designation_span else ""
            )

            title, court_name = self._split_designation(
                designation
            )

            image_url = None

            image_div = card.find("div", class_="person_image")
            if image_div:
                img = image_div.find("img")
                if img:
                    image_url = img.get("src")

            institution_name = (
                f"{court_name} of Kenya"
                if court_name else
                "Judiciary of Kenya"
            )

            if institution_name not in institution_cache:
                institution = Institution(
                    institution_name=institution_name,
                    category="Judiciary",
                    country="Kenya"
                )
                institution_cache[institution_name] = institution
                result.institutions.append(institution)
            else:
                institution = institution_cache[institution_name]

            position_title = title or "Judge"

            if position_title not in position_cache:
                position = Position(
                    title=position_title,
                    category="Judiciary"
                )
                position_cache[position_title] = position
                result.positions.append(position)
            else:
                position = position_cache[position_title]

            person = Person(
                full_name=full_name,
                is_pep=True,
                confidence_score=97.0,
                entity_type="PERSON",
                primary_source=source_document.source_name,
                status="ACTIVE",
                nationality="Kenyan",
                country="Kenya",
                profile_url=profile_url or "",
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
            f"Extracted {len(result.persons)} judges."
        )

        return result

    def _split_designation(self, designation):
        """
        Split a designation string into (title, canonical_court).

        Handles all observed formats:

            "Judge, Court of Appeal"
                -> ("Judge", "Court of Appeal")

            "Chief Justice and President of the Supreme Court of Kenya"
                -> ("Chief Justice and President", "Supreme Court")

            "judge of the ELRC"
                -> ("Judge", "Employment and Labour Relations Court")

        Returns ("", "") if no known court name is found anywhere
        in the string -- nothing is silently dropped in that case,
        the raw designation is returned as the title instead.
        """

        if not designation:
            return "", ""

        for alias in sorted(COURT_ALIASES, key=len, reverse=True):

            idx = designation.find(alias)

            if idx == -1:
                continue

            canonical = COURT_ALIASES[alias]

            title = designation[:idx].rstrip()

            changed = True
            while changed:
                changed = False
                for connector in TRAILING_CONNECTORS:
                    if title.endswith(connector):
                        title = title[: -len(connector)].rstrip()
                        changed = True

            title = title.strip(" ,")

            if not title:
                title = "Judge"

            if title[0].islower():
                title = title[0].upper() + title[1:]

            return title, canonical

        return designation, ""
