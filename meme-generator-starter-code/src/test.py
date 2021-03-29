from QuoteEngine import Ingestor

quotes = Ingestor.parse("src/_data/DogQuotes/DogQuotesDOCX.docx")

for quote in quotes:
    print(quote)

# from MemeGenerator import MemeGenerator

# mg = MemeGenerator("memes/")
# mg.make_meme(
#     "src/_data/photos/dog/xander_2.jpg",
#     text="Life's a bitch and then you die",
#     author="Nas",
#     width=400,
# )
