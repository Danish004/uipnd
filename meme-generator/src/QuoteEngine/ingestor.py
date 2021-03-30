from typing import List
from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel
from .csv_ingestor import CSVIngestor
from .pdf_ingestor import PDFIngestor
from .docx_ingestor import DocxIngestor
from .txt_ingestor import TxtIngestor
from beartype import beartype


class Ingestor(IngestorInterface):
    """Selects the appropriate helper class to parse the file."""

    ingestors = [CSVIngestor, PDFIngestor, DocxIngestor, TxtIngestor]

    @classmethod
    @beartype
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parses the file with correct ingestor.

        Args:
            path (str): Path to file.

        Returns:
            List[QuoteModel]: List of QuoteModel objects.
        """
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)