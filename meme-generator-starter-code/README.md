# Meme Generator

An app that generates memes. Memes can either be created randomly (by randomly picking an image and a quote from a predefined data pool) or by user input (quote & image url).

This app was built with the [Flask](https://palletsprojects.com/p/flask/)
web application framework.

## Setup

In the root directory run the following command: `source venv/bin/activate` to activate the virtual environment that also includes all project dependencies. Run `deactivate` to deactivate the virtual environment.

You can also create a virtual environment on your own, either with venv or with conda. With that environment activated, navigate to the root directory and run `pip install -r requirements.txt`.

You also need to install `pdftotext` from here:

- Windows: https://www.xpdfreader.com/download.html
- Debian: `sudo apt-get update && sudo apt-get install -y xpdf`
- macOS: `brew install --cask pdftotext`

## Run

To start the app navigate to `/src` and run `python3 app.py`. The frontend can be accessed at: http://127.0.0.1:5000/.

## Project Interface

The project consists of 2 basic modules:

- `QuoteEngine`
- `MemeGenerator`

### Quote Engine

This module contains all the classes responsible for parsing quotes from different types of data (csv, docx, pdf & txt) and assigning them to a `QuoteModel`.

#### quote_model.py

Contains the main class `QuoteModel` that represents a single quote and holds the information of the body and the author of that specific quote.

#### ingestor_interface.py

Contains the main base class that further classes inherit from, to serve a certain functionality based on the type of data that is to be parsed. These are the following:

- `CSVIngestor` that can be found in `csv_ingestor.py`.
- `DocxIngestor` that can be found in `docx_ingestor.py`.
- `TxtIngestor` that can be found in `txt_ingestor.py`.
- `PDFIngestor` that can be found in `pdf_ingestor.py`.

#### ingestor.py

Contains `Ingestor`, a class that encapsulates the aforementioned derived classes' functionality and is responsible for the selection of the appropriate helper class for parsing the data. It finally returns a list of `QuoteModel` objects.

A typical example on the use of `Ingestor` is the following:

```python
from QuoteEngine import Ingestor

quotes = Ingestor.parse("./_data/DogQuotes/DogQuotesDOCX.docx")

# returns a list of QuoteModel objects
for quote in quotes:
    print(quote)
```

### Meme Generator

This module contains the `MemeEngine` class that is responsible for generating a meme for a given image and a quote (text/body and author).

The use of `MemeEngine` is pretty straightforward:

```python
from MemeGenerator import MemeGenerator

# intantiate a MemeGenerator with a given output directory
mg = MemeGenerator("memes/")

# generate meme from a given image and a quote
mg.make_meme(
    "src/_data/photos/dog/xander_2.jpg",
    text="Life's a bitch and then you die",
    author="Nas",
    width=400,
)
```

## Flask app

The Flask app consists of 2 components:

- meme.py
- app.py

### meme.py

This script encapsulates `MemeEngine`'s functionality by additionally providing accessibility via the command line. At a command line you can run `python meme.py --help` for an explanation on how to invoke the script.

```console
usage: meme.py [-h] [--body BODY] [--author AUTHOR] [--path PATH]

Generate meme.

optional arguments:
  -h, --help       show this help message and exit
  --body BODY      Quote body.
  --author AUTHOR  Quote author.
  --path PATH      Image path.

```

### app.py

A typical Flask template script that provides the following endpoints for the user to interact with the frontent (http://127.0.0.1:5000/):

- `/`: The homepage that includes the main html form for random meme generation (`./src/templates/meme.html`). It picks a random image and a quote from `./src/_data/` and generates a meme with a `MemeEngine` object.
- `/create`: Provides the ability to generate a custom meme from a given image url and a quote. Consists of the following stages:
  - `GET`: The GET request gets the user data from the html form that user completes (`./src/templates/meme.html`), consisting of the following areas: `image url`, `Quote Body` & `Quote Author`.
  - `POST`: Once the form is filled the POST request is used to send the user data to the server in order to finally generate the meme.
