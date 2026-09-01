from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from parsers.base_parser import BaseParser


class BaseHTMLParser(BaseParser):
    """
    Base class for HTML parsers.

    Provides common HTML parsing utilities used by all
    government website parsers.
    """

    def __init__(self, parser_name: str):

        super().__init__(parser_name)

    # ---------------------------------------------------------

    def load_html(self, source_document):

        self.logger.info(
            f"Loading {source_document.raw_path}"
        )

        html = Path(
            source_document.raw_path
        ).read_text(
            encoding="utf-8",
            errors="ignore"
        )

        return html

    # ---------------------------------------------------------

    def create_soup(self, html):

        return BeautifulSoup(
            html,
            "html.parser"
        )

    # ---------------------------------------------------------

    def clean_text(self, text):

        if text is None:
            return ""

        return " ".join(
            text.strip().split()
        )

    # ---------------------------------------------------------

    def text(self, element):

        if element is None:
            return ""

        return self.clean_text(
            element.get_text(" ")
        )

    # ---------------------------------------------------------

    def attr(self, element, attribute):

        if element is None:
            return ""

        return element.get(attribute, "")

    # ---------------------------------------------------------

    def absolute_url(self, base_url, href):

        if not href:
            return ""

        return urljoin(base_url, href)

    # ---------------------------------------------------------

    def select_one_text(self, parent, selector):

        element = parent.select_one(selector)

        return self.text(element)

    # ---------------------------------------------------------

    def select_all(self, soup, selector):

        return soup.select(selector)