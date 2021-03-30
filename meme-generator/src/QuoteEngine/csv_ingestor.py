from typing import List
from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel
import pandas as pd
from beartype import beartype


class CSVIngestor(IngestorInterface):
    """Ingests a .csv file."""

    allowed_extensions = ["csv"]

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

        df = pd.read_csv(path, header=0)
        return [
            QuoteModel(f"'{body}'", author)
            for body, author in zip(df["body"], df["author"])
        ]
