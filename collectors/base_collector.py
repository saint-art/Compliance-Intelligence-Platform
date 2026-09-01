from pathlib import Path
from time import perf_counter
import hashlib

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from models.source_document import SourceDocument
from utils.logger import get_logger


class BaseCollector:
    """
    Base collector used by every HTTP source.

    Supports:

    - Single-page collectors
    - Paginated collectors
    - Immutable HTML source snapshots
    - SHA-256 content checksums
    - Retry-enabled HTTP requests

    Every unique downloaded document is stored as an immutable
    content-addressed snapshot.

    Example:

        input/raw_html/
            cabinet_<checksum>.html
            presidency_<checksum>.html

    If the exact same content is collected again, the same snapshot
    path is reused instead of overwriting the previous snapshot.
    """

    def __init__(
        self,
        source_name,
        url,
        timeout=30,
        retries=3,
    ):

        self.source_name = source_name
        self.url = url
        self.timeout = timeout

        self.logger = get_logger(source_name)

        self.headers = {
            "User-Agent": (
                "Compliance-Intelligence-Platform/1.0"
            )
        }

        self.session = requests.Session()

        retry = Retry(
            total=retries,
            backoff_factor=1,
            status_forcelist=[
                429,
                500,
                502,
                503,
                504
            ],
            allowed_methods=["GET"]
        )

        adapter = HTTPAdapter(
            max_retries=retry
        )

        self.session.mount(
            "https://",
            adapter
        )

        self.session.mount(
            "http://",
            adapter
        )

    # ---------------------------------------------------------
    # HTTP DOWNLOAD
    # ---------------------------------------------------------

    def download(self, url=None):
        """
        Download one URL.

        Returns:

            html,
            HTTP status code,
            elapsed seconds
        """

        target = url or self.url

        self.logger.info(
            f"Downloading: {target}"
        )

        start = perf_counter()

        response = self.session.get(
            target,
            headers=self.headers,
            timeout=self.timeout
        )

        response.raise_for_status()

        elapsed = round(
            perf_counter() - start,
            2
        )

        self.logger.info(
            f"Download completed "
            f"(HTTP {response.status_code}, "
            f"{elapsed}s)"
        )

        return (
            response.text,
            response.status_code,
            elapsed
        )

    # ---------------------------------------------------------
    # CHECKSUM
    # ---------------------------------------------------------

    def calculate_checksum(self, html):
        """
        Calculate SHA-256 checksum for the downloaded content.
        """

        return hashlib.sha256(
            html.encode("utf-8")
        ).hexdigest()

    # ---------------------------------------------------------
    # SNAPSHOT FILENAME
    # ---------------------------------------------------------

    def snapshot_filename(
        self,
        filename,
        checksum
    ):
        """
        Generate an immutable content-addressed filename.

        Example:

            cabinet.html

        becomes:

            cabinet_<checksum>.html
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
        html,
        filename,
        checksum=None
    ):
        """
        Save HTML as an immutable source snapshot.

        The checksum is calculated before selecting the final
        filename, ensuring that different document versions can
        never overwrite one another.
        """

        if checksum is None:
            checksum = self.calculate_checksum(
                html
            )

        folder = Path(
            "input/raw_html"
        )

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        snapshot_name = self.snapshot_filename(
            filename,
            checksum
        )

        path = folder / snapshot_name

        # Exact content already exists.
        # Do not rewrite it unnecessarily.
        if path.exists():

            self.logger.info(
                f"Snapshot already exists: {path}"
            )

            return path

        # Write through a temporary file first.
        # This prevents partially-written snapshots
        # from being treated as valid source documents.
        temp_path = path.with_suffix(
            path.suffix + ".tmp"
        )

        temp_path.write_text(
            html,
            encoding="utf-8",
            errors="ignore"
        )

        temp_path.replace(path)

        self.logger.info(
            f"Saved immutable HTML snapshot -> {path}"
        )

        return path

    # ---------------------------------------------------------
    # CREATE SOURCE DOCUMENT
    # ---------------------------------------------------------

    def download_page(
        self,
        url,
        filename
    ):
        """
        Download one page and convert it into
        a SourceDocument backed by an immutable
        HTML snapshot.
        """

        html, _, _ = self.download(
            url
        )

        checksum = self.calculate_checksum(
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

    # ---------------------------------------------------------
    # DEFAULT COLLECTION
    # ---------------------------------------------------------

    def collect(self):

        filename = (
            self.source_name.lower()
            .replace(" ", "_")
            + ".html"
        )

        return self.download_page(
            self.url,
            filename
        )