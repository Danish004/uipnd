# Meme Generator

A Flask app that generates memes. The memes can either be created randomly or by user input (quote & image url).

## Setup

In the root directory run the following command: `source venv/bin/activate` to activate the virtual environment that also includes all project dependencies. Run `deactivate` to deactivate the virtual environment.

You can also create a venv on your own. With that environment activated navigate to the root directory and type `pip install -r requirements.txt`.

You also need to install `pdftotext` from here:

- Windows: https://www.xpdfreader.com/download.html
- Debian: `sudo apt-get update && sudo apt-get install -y xpdf`
- macOS: `brew install --cask pdftotext`

## Run

To start the app navigate to `/src` and run `python3 app.py`. The frontend can be accessed at: http://127.0.0.1:5000/.
