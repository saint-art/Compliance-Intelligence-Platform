from abc import ABC, abstractmethod

from utils.logger import get_logger


class BaseParser(ABC):
    """
    Base interface for every source parser.

    Every parser receives a SourceDocument and returns
    a ParserResult containing extracted entities and
    relationships.
    """

    def __init__(self, parser_name: str):

        self.logger = get_logger(parser_name)

    @abstractmethod
    def parse(self, source_document):
        """
        Parse one SourceDocument.

        Returns
        -------
        ParserResult
            Extracted entities and relationships.
        """

        raise NotImplementedError