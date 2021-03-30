from PIL import Image, ImageDraw, ImageFont
import os
import random
from beartype import beartype


class MemeEngine:
    """Generates meme from a given image."""

    @beartype
    def __init__(self, output_dir: str):
        """Instantiate a MemeGenerator object.

        Args:
            output_dir (str): Output directory to save memes.
        """

        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir

    @beartype
    def _load_image(self, img_path: str):
        """Loads an image to an Image object.

        Args:
            img_path (str): Path to image.
        """

        return Image.open(img_path)

    @beartype
    def _resize(self, img, width: int):
        """Resize image to a given width and maintain aspect ratio.

        Args:
            width (int): Width pixel size.
        """

        ratio = img.size[1] / img.size[0]  # height / width
        new_width = width
        new_height = int(new_width * ratio)
        img = img.resize((new_width, new_height), Image.ANTIALIAS)

        return img

    @beartype
    def _add_caption(self, img, text: str, author: str):
        """Adds caption (text and author) to the modified image.

        Args:
            text (str): Body of meme.
            author (str): Author of meme.
        """

        # fit text to image
        fontsize = 1
        img_fraction = 0.5
        fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", fontsize)
        while fnt.getsize(text)[0] < img_fraction * img.size[0]:
            # iterate until the text size is just larger than the criteria
            fontsize += 1
            fnt = ImageFont.truetype(
                "Pillow/Tests/fonts/FreeMono.ttf", fontsize
            )

        # draw text
        d = ImageDraw.Draw((img))
        d.text((0, 0), f"{text} - {author}", font=fnt, fill=(0, 0, 0, 0))

        return img

    @beartype
    def make_meme(
        self, img_path: str, text: str, author: str, width=500
    ) -> str:
        """Make meme from a given image and a quote.

        Args:
            img_path (str): Path to image.
            text (str): Body of quote.
            author (str): Author of quote.
            width (int, optional): Width of modified image in pixels. Defaults to 500.

        Returns:
            str: Path of saved meme.
        """

        img = self._load_image(img_path)
        img = self._resize(img, width)
        img = self._add_caption(img, text, author)

        original_name = img_path.split(".jpg")[0].split("/")[-1]
        save_path = os.path.join(
            self.output_dir,
            f"{original_name}_modified_{random.randint(0, 1000000000)}.jpg",
        )
        img.save(save_path)

        return save_path