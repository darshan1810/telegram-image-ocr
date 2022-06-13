from concurrent.futures import process
import pytesseract
from PIL import Image
from PIL import ImageFilter


def process_image(path):
    image = get_image(path)
    image.filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(image)


def get_image(path):
    return Image.open(path)


if __name__ == "__main__":
    print(process_image("img/"))
