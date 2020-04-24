from PIL import Image, ImageChops
from pytesseract import image_to_string
from mtgsdk import Card, Set, Type, Supertype, Subtype, Changelog

card = Image.open('card_5.png')

name_area = (20, 20, 210, 40)
name = card.crop(name_area)

text_area = (20, 41, 210, 200)
text = card.crop(text_area)

print(image_to_string(text))
text.show()
print(image_to_string(name))