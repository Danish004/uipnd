class QuoteModel:
    """Stores body and author of a given quote."""

    def __init__(self, body, author):
        """Instantiates a QuoteModel object.

        Args:
            body (str): Body of the quote.
            author (str): Author of the quote.
        """
        self.body = body
        self.author = author

    def __str__(self):
        """Prints the quote.

        Returns:
            [str]: The quote.
        """
        return f"{self.body} - {self.author}"