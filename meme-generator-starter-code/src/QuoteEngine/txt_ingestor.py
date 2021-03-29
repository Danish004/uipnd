from typing import List
from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel
from beartype import beartype


class TxtIngestor(IngestorInterface):
    """Ingests a .txt file."""

    allowed_extensions = ["txt"]

    @classmethod
    @beartype
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parses the content of a path to return a list of QuoteModel objects.

        Args:
            path (str): Path to file.

        Returns:
            List[QuoteModel]: List[QuoteModel]: List of QuoteModel objects.
        """
        if not cls.can_ingest(path):
            raise Exception("cannot ingest exception")

        quotes = []

        with open(path, "r") as f:
            for line in f.readlines():
                line = line.strip("\n\r").strip()
                if len(line) > 0:
                    body, author = line.split(" - ")
                    quotes.append(QuoteModel(f"'{body}'", author))
        return quotes