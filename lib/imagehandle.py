# -*- UTF-8 -*-

import sys

from PIL import Image,ImageGrab
import pytesseract

reload(sys)
sys.setdefaultencoding('utf-8')

img = ImageGrab.grab()
img.save('../file/0.png')
img = Image.open('../file/1.png')
text = pytesseract.image_to_string(img, lang='eng')
print text
