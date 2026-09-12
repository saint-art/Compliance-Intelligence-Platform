import re
from pathlib import Path

from bs4 import BeautifulSoup

from parsers.base_parser import BaseParser
from parsers.parser_result import ParserResult

from models.person import Person
from models.position import Position
from models.institution import Institution
from models.person_position import PersonPosition


PAREN_PATTERN = re.compile(r'\(([^()]*)\)')

TITLE_KEYWORDS = [
    "director", "chairman", "chairperson", "secretary",
    "officer", "manager", "chief", "executive",
]


class KPLCParser(BaseParser):
    """
    Parses the Kenya Power (KPLC) Board of Directors page.

    Structure: Tailwind-styled cards, one per board member, with
    name and title combined in a single text node:

        div.text-lg.font-bold.text-white
            "Name, Title (extra detail)"
            or
            "Name (Title)"
            or
            "Name (Title), credentials..."

    The source data is genuinely inconsistent in how name and
    title are combined (sometimes comma-separated, sometimes
    parenthetical, sometimes both) -- _split_name_title() handles
    every observed variant by locating the first parenthetical
    group that contains a recognizable title keyword, then
    deciding whether a preceding comma marks the name/title
    boundary instead.

    No <img> tag is present -- photos are set via CSS
    background-image on the card container, not extracted here.
    """

    def __init__(self):
        super().__init__("KPLCParser")

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
            institution_name="Kenya Power and Lighting Company",
            category="State Corporation",
            country="Kenya"
        )
        result.institutions.append(institution)

        position_cache = {}

        name_divs = soup.select("div.text-lg.font-bold.text-white")

        self.logger.info(
            f"Found {len(name_divs)} board member card(s)."
        )

        for div in name_divs:

            raw_text = div.get_text(" ", strip=True)

            if not raw_text:
                continue

            full_name, position_title = self._split_name_title(
                raw_text
            )

            if not full_name:
                continue

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
                country="Kenya"
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
            f"Extracted {len(result.persons)} KPLC board members."
        )

        return result

    def _split_name_title(self, text):
        """
        See class docstring. Returns (name, title). If no
        recognizable title keyword is found anywhere, the whole
        string is returned as the name and title is set to
        "Unknown Position" (nothing is silently dropped).
        """

        anchor = None

        for match in PAREN_PATTERN.finditer(text):

            content = match.group(1)

            if any(k in content.lower() for k in TITLE_KEYWORDS):
                anchor = match
                break

        if anchor is None:
            return text.strip(), "Unknown Position"

        comma_idx = text.find(",")

        if comma_idx != -1 and comma_idx < anchor.start():

            name = text[:comma_idx].strip()
            title = text[comma_idx + 1: anchor.end()].strip()

        else:

            name = text[:anchor.start()].strip()
            title = anchor.group(1).strip()

        return name, title
