from abc import ABC, abstractmethod


class BaseResolver(ABC):
    """
    Base class for all entity resolvers.

    A resolver decides whether an extracted entity should

    • create a new record

    • update an existing record

    • be ignored

    before the repository performs persistence.
    """

    @abstractmethod
    def resolve(self, parser_result):
        pass