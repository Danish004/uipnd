from typing import List
import docx
from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel
import docx
from beartype import beartype


class DocxIngestor(IngestorInterface):
    """Ingests a .docx file."""

    allowed_extensions = ["docx"]

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
        doc = docx.Document(path)

        for para in doc.paragraphs:
            if para.text != "":
                body, author = para.text.split(" - ")
                quotes.append(QuoteModel(body, author))

        return quotes