import random
import os
import shutil
import requests
from flask import (
    Flask,
    render_template,
    abort,
    request,
    flash,
    redirect,
    url_for,
)
from MemeGenerator import MemeEngine
from QuoteEngine import Ingestor, QuoteModel

app = Flask(__name__)
app.secret_key = "a random secret key"

meme = MemeEngine("./static")


def setup():
    """ Load all resources """

    # helps setting the paths differently when debugging with vscode
    cwd = os.getcwd()
    cwd = cwd.split("/")[-1]
    if cwd == "meme-generator":
        quote_files = [
            "./src/_data/DogQuotes/DogQuotesTXT.txt",
            "./src/_data/DogQuotes/DogQuotesDOCX.docx",
            "./src/_data/DogQuotes/DogQuotesPDF.pdf",
            "./src/_data/DogQuotes/DogQuotesCSV.csv",
        ]
        images_path = "./src/_data/photos/dog/"
    elif cwd == "src":
        quote_files = [
            "./_data/DogQuotes/DogQuotesTXT.txt",
            "./_data/DogQuotes/DogQuotesDOCX.docx",
            "./_data/DogQuotes/DogQuotesPDF.pdf",
            "./_data/DogQuotes/DogQuotesCSV.csv",
        ]
        images_path = "./_data/photos/dog/"

    quotes = []
    for f in quote_files:
        if not os.path.exists(f):
            print(f"The following quote sample is missing: {f}")
            continue
        quotes.extend(Ingestor.parse(f))

    if not quotes:
        raise Exception("No sample quotes found!")

    imgs = []
    for root, dirs, files in os.walk(images_path):
        imgs = [os.path.join(root, name) for name in files]
        for img in imgs:
            if not os.path.exists(img):
                print("The following image sample is missing: ", img)
                imgs.remove(img)
                continue

    if not imgs:
        raise Exception("No sample images found!")

    return quotes, imgs


quotes, imgs = setup()


@app.route("/")
def meme_rand():
    """Generate a random meme."""
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)

    return render_template("meme.html", path=path)


@app.route("/create", methods=["GET"])
def meme_form():
    """User input for meme information."""
    return render_template("meme_form.html")


@app.route("/create", methods=["POST"])
def meme_post():
    """Create a user defined meme."""
    img_url = request.form.get("image_url")
    try:
        response = requests.get(img_url, stream=True)
    except requests.exceptions.RequestException:
        flash("Please enter a valid Image URL!")
        return redirect(url_for("meme_form"))

    img_path = f"./img_{random.randint(0, 10000000)}.jpg"
    with open(img_path, "wb") as f:
        f.write(response.content)

    body = request.form.get("body", "")
    if body:
        body = f"'{body}'"
    author = request.form.get("author", "")
    quote = QuoteModel(body, author)  # it's not really needed

    try:
        print(quote)
        path = meme.make_meme(img_path, quote.body, quote.author)
    except:
        flash("Please enter a Quote Body and Quote Author!")
        if os.path.exists(img_path):
            os.remove(img_path)
        return redirect(url_for("meme_form"))

    if os.path.exists(img_path):
        os.remove(img_path)

    return render_template("meme.html", path=path)


if __name__ == "__main__":
    app.run()
