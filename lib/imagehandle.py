# -*- coding: UTF-8 -*-

import sys

from PIL import Image, ImageGrab
import pytesseract

reload(sys)
sys.setdefaultencoding('utf-8')

# img = ImageGrab.grab()
# img.save('../file/0.png')
img = Image.open('../file/1.jpg').convert('L')

img = Image.eval(img, lambda i: i * 2)  # 将原图片的像素点，都乘2，返回的是一个Image对象
img.save('../file/2.png')
text = pytesseract.image_to_string(img, lang='eng')
print text
