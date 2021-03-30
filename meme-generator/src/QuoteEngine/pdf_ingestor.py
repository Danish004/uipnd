from typing import List
import subprocess
import os
import random
from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel
from beartype import beartype


class PDFIngestor(IngestorInterface):
    """Ingests a .pdf file."""

    allowed_extensions = ["pdf"]

    @classmethod
    @beartype
    def parse(cls, path: str) -> List[QuoteModel]:
        """Converts the path to .txt file and parses the content to return a list of QuoteModel objects.

        Args:
            path (str): Path to file.

        Raises:
            Exception: If the .pdf is not found.

        Returns:
            List[QuoteModel]: List[QuoteModel]: List of QuoteModel objects.
        """
        if not cls.can_ingest(path):
            raise Exception("cannot ingest exception")

        quotes = []

        os.makedirs("./tmp", exist_ok=True)
        tmp = f"./tmp/{random.randint(0, 10000000)}.txt"

        try:
            call = subprocess.call(["pdftotext", path, tmp])
        except:
            print(path, "not found!")

        with open(tmp, "r") as f:
            for line in f.readlines():
                line = line.strip("\n\r").strip()
                if len(line) > 0:
                    body, author = line.split(" - ")
                    quotes.append(QuoteModel(body, author))

        if os.path.exists(tmp):
            os.remove(tmp)

        return quotes