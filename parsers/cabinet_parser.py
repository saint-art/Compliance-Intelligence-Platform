from bs4 import BeautifulSoup
from urllib.parse import urljoin

from parsers.base_parser import BaseParser
from parsers.parser_result import ParserResult

from models.person import Person
from models.position import Position
from models.institution import Institution
from models.person_position import PersonPosition



BASE_URL = "https://www.president.go.ke"


class CabinetParser(BaseParser):

    def __init__(self):
        super().__init__("CabinetParser")

    def parse(self, source_document):

        self.logger.info(
            f"Loading {source_document.raw_path}"
        )

        with open(
            source_document.raw_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            soup = BeautifulSoup(
                f,
                "html.parser"
            )

        result = ParserResult(
            source_document=source_document
        )

        # -----------------------------------------------------
        # INSTITUTION
        # -----------------------------------------------------

        cabinet = Institution(

            institution_name="Cabinet of Kenya",

            category="Executive",

            country="Kenya"

        )

        result.institutions.append(
            cabinet
        )

        # -----------------------------------------------------
        # CARDS
        # -----------------------------------------------------

        cards = soup.select(
            "div.brxe-kvyrtk[href]"
        )

        self.logger.info(
            f"Found {len(cards)} cabinet cards."
        )

        for card in cards:

            # -------------------------------------------------
            # PROFILE URL
            # -------------------------------------------------

            href = card.get("href")

            profile_url = None

            if href:

                profile_url = urljoin(
                    BASE_URL,
                    href
                )

            # -------------------------------------------------
            # IMAGE
            # -------------------------------------------------

            image = card.find("img")

            image_url = None

            if image:

                image_url = (
                    image.get("data-src")
                    or image.get("src")
                )

                if image_url:

                    image_url = urljoin(
                        BASE_URL,
                        image_url
                    )

            # -------------------------------------------------
            # NAME
            # -------------------------------------------------

            heading = card.find("h6")

            if heading is None:

                continue

            full_name = heading.get_text(
                " ",
                strip=True
            )

            # -------------------------------------------------
            # POSITION
            # -------------------------------------------------

            position_node = card.find(
                "div",
                class_="brxe-evvnhh"
            )

            if position_node is None:

                continue

            position_title = position_node.get_text(
                " ",
                strip=True
            )

            # -------------------------------------------------
            # PERSON
            # -------------------------------------------------

            person = Person(

                full_name=full_name,

                profile_url=profile_url,

                image_url=image_url,

                is_pep=True,

                confidence_score=97.0,

                entity_type="PERSON",

                primary_source=(
                    source_document.source_name
                ),

                status="ACTIVE"

         )

            result.persons.append(
                person
            )

            # -------------------------------------------------
            # POSITION
            # -------------------------------------------------

            position = Position(

                title=position_title,

                category="Cabinet"

            )

            result.positions.append(
                position
            )

            # -------------------------------------------------
            # RELATIONSHIP
            # -------------------------------------------------

            relationship = PersonPosition(

                confidence_score=100.0,

                is_current=True,

                source_document_id=(
                    source_document.document_id
                ),

                person=person,

                position=position,

                institution=cabinet

            )

            result.relationships.append(
                relationship
            )

        # -----------------------------------------------------
        # SUMMARY
        # -----------------------------------------------------

        self.logger.info(

            f"Extracted "

            f"{len(result.persons)} persons, "

            f"{len(result.positions)} positions, "

            f"{len(result.institutions)} institutions, "

            f"{len(result.relationships)} relationships."

        )

        return result