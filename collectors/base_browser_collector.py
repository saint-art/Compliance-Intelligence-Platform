from pathlib import Path
from time import perf_counter
import hashlib

from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError
)

from models.source_document import SourceDocument
from utils.logger import get_logger


class BaseBrowserCollector:
    """
    Base collector for JavaScript-driven websites.

    Uses Playwright to render pages before saving HTML.

    Every unique rendered document is stored as an immutable,
    content-addressed snapshot.
    """

    RAW_HTML_DIR = Path("input/raw_html")

    def __init__(
        self,
        source_name: str,
        timeout: int = 30000,
        headless: bool = True
    ):
        self.source_name = source_name
        self.timeout = timeout
        self.headless = headless

        self.logger = get_logger(
            source_name
        )

    # ---------------------------------------------------------
    # RENDER PAGE
    # ---------------------------------------------------------

    def render_page(self, url: str):
        """
        Render a JavaScript-driven page using Playwright
        and return the final HTML.
        """

        self.logger.info(
            f"Rendering: {url}"
        )

        start = perf_counter()

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=self.headless
            )

            try:

                page = browser.new_page()

                try:
                    page.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=self.timeout
                    )
                except PlaywrightTimeoutError:
                    
                    self.logger.warning(
                        f"Navigation timeout for {url}. "
                        "Attempting to capture the current page content."
                    )
                

                html = page.content()

            finally:
                browser.close()

        elapsed = round(
            perf_counter() - start,
            2
        )

        self.logger.info(
            f"Rendered in {elapsed}s"
        )

        return html

    # ---------------------------------------------------------
    # CHECKSUM
    # ---------------------------------------------------------

    def checksum(self, html: str) -> str:
        """
        Generate a SHA-256 checksum for rendered HTML.

        The checksum is used as the immutable content identity
        of the snapshot.
        """

        return hashlib.sha256(
            html.encode("utf-8")
        ).hexdigest()

    # ---------------------------------------------------------
    # SNAPSHOT FILENAME
    # ---------------------------------------------------------

    def snapshot_filename(
        self,
        filename: str,
        checksum: str
    ) -> str:
        """
        Generate an immutable content-addressed filename.

        Example:

            source.html

        becomes:

            source_<checksum>.html
        """

        original = Path(filename)

        stem = original.stem
        suffix = original.suffix or ".html"

        return (
            f"{stem}_{checksum}{suffix}"
        )

    # ---------------------------------------------------------
    # SAVE IMMUTABLE SNAPSHOT
    # ---------------------------------------------------------

    def save_html(
        self,
        html: str,
        filename: str,
        checksum: str = None
    ):
        """
        Save rendered HTML as an immutable snapshot.

        If a checksum is not supplied, it is calculated here.

        The filename is content-addressed, meaning the same
        HTML content always maps to the same snapshot filename.
        """

        if not isinstance(html, str):
            raise TypeError(
                "html must be a string."
            )

        if not html:
            raise ValueError(
                "Cannot save an empty HTML document."
            )

        if checksum is None:
            checksum = self.checksum(
                html
            )

        expected_checksum = self.checksum(
            html
        )

        if checksum != expected_checksum:
            raise ValueError(
                "Provided checksum does not match "
                "the supplied HTML content."
            )

        output = self.RAW_HTML_DIR

        output.mkdir(
            parents=True,
            exist_ok=True
        )

        snapshot_name = self.snapshot_filename(
            filename,
            checksum
        )

        path = output / snapshot_name

        # -----------------------------------------------------
        # IMMUTABILITY
        # -----------------------------------------------------
        #
        # If the exact same content-addressed snapshot already
        # exists, leave it untouched.
        #
        # If a file with the same checksum somehow contains
        # different content, fail loudly instead of overwriting.
        #

        if path.exists():

            existing_html = path.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            existing_checksum = self.checksum(
                existing_html
            )

            if existing_checksum != checksum:
                raise IOError(
                    "Snapshot filename collision detected: "
                    f"{path}"
                )

            self.logger.info(
                f"Immutable HTML snapshot already exists -> {path}"
            )

            return path

        path.write_text(
            html,
            encoding="utf-8"
        )

        self.logger.info(
            f"Saved immutable HTML snapshot -> {path}"
        )

        return path

    # ---------------------------------------------------------
    # DOWNLOAD / RENDER PAGE
    # ---------------------------------------------------------

    def download_page(
        self,
        url: str,
        filename: str
    ):
        """
        Render a page, save its immutable HTML snapshot,
        and return a SourceDocument describing that snapshot.
        """

        if not url:
            raise ValueError(
                "url is required."
            )

        if not filename:
            raise ValueError(
                "filename is required."
            )

        html = self.render_page(
            url
        )

        checksum = self.checksum(
            html
        )

        path = self.save_html(
            html,
            filename,
            checksum=checksum
        )

        document = SourceDocument(
            source_name=self.source_name,

            source_type="HTML",

            source_url=url,

            title=Path(filename).stem,

            document_type="HTML",

            raw_path=str(path),

            checksum=checksum
        )

        self.logger.info(
            f"Created SourceDocument "
            f"{document.document_id}"
        )

        return document
