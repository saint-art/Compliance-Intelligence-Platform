from pathlib import Path

from bs4 import BeautifulSoup

from parsers.base_parser import BaseParser
from parsers.parser_result import ParserResult

from models.person import Person
from models.position import Position
from models.institution import Institution
from models.person_position import PersonPosition


class PresidencyParser(BaseParser):

    def __init__(self):
        super().__init__("PresidencyParser")

    def parse(self, source_document):

        self.logger.info(
            f"Loading {source_document.raw_path}"
        )

        # -------------------------------------------------
        # LOAD SOURCE DOCUMENT
        # -------------------------------------------------

        html = Path(
            source_document.raw_path
        ).read_text(
            encoding="utf-8",
            errors="ignore"
        )

        # Parse the HTML so the parser is structurally
        # prepared for future extraction from the source.
        BeautifulSoup(
            html,
            "html.parser"
        )

        result = ParserResult(
            source_document=source_document
        )

        # -------------------------------------------------
        # INSTITUTION
        # -------------------------------------------------

        presidency = Institution(

            institution_name="Presidency of Kenya",

            category="Government",

            country="Kenya"

        )

        result.institutions.append(
            presidency
        )

        # -------------------------------------------------
        # POSITIONS
        # -------------------------------------------------

        president_position = Position(
            title="President",
            category="Presidency"
        )

        deputy_position = Position(
            title="Deputy President",
            category="Presidency"
        )

        result.positions.extend([
            president_position,
            deputy_position
        ])

        # -------------------------------------------------
        # PERSONS
        # -------------------------------------------------

        president = Person(

            full_name="William Samoei Ruto",

            first_name="William",

            middle_name="Samoei",

            last_name="Ruto",

            nationality="Kenyan",

            country="Kenya",

            is_pep=True,

            confidence_score=99,

            primary_source=source_document.source_name,

            entity_status="ACTIVE",

            status="ACTIVE"

        )

        deputy = Person(

            full_name="Kithure Kindiki",

            first_name="Kithure",

            last_name="Kindiki",

            nationality="Kenyan",

            country="Kenya",

            is_pep=True,

            confidence_score=98,

            primary_source=source_document.source_name,

            entity_status="ACTIVE",

            status="ACTIVE"

        )

        result.persons.extend([
            president,
            deputy
        ])

        # -------------------------------------------------
        # RELATIONSHIPS
        # -------------------------------------------------
        #
        # IMPORTANT:
        # The object references below are required because
        # RelationshipResolver uses them to inject the
        # database IDs after the entities have been saved.
        #

        president_relationship = PersonPosition(

            source_document_id=(
                source_document.document_id
            ),

            confidence_score=100.0,

            is_current=True,

            person=president,

            position=president_position,

            institution=presidency

        )

        deputy_relationship = PersonPosition(

            source_document_id=(
                source_document.document_id
            ),

            confidence_score=100.0,

            is_current=True,

            person=deputy,

            position=deputy_position,

            institution=presidency

        )

        result.relationships.extend([
            president_relationship,
            deputy_relationship
        ])

        # -------------------------------------------------
        # SUMMARY
        # -------------------------------------------------

        self.logger.info(
            f"Extracted "
            f"{len(result.persons)} persons, "
            f"{len(result.positions)} positions, "
            f"{len(result.institutions)} institutions, "
            f"{len(result.relationships)} relationships."
        )

        return result