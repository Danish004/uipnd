from typing import List
from abc import ABC, abstractmethod
from .quote_model import QuoteModel
from beartype import beartype


class IngestorInterface:
    """Base class the all ingestors should inherit from."""

    allowed_extensions = []

    @classmethod
    @beartype
    def can_ingest(cls, path: str) -> bool:
        """Checks if the given path is in the list of allowed extensions."""

        ext = path.split(".")[-1]
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    @beartype
    def parse(cls, path: str) -> List[QuoteModel]:
        """Abstract method for parsing a path."""
        pass