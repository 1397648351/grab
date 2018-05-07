# -*-coding:utf-8-*-

import sys
from PIL import Image, ImageGrab
import pytesseract

reload(sys)
sys.setdefaultencoding("utf-8")

filepath = 'file/4.jpg'
img = Image.open(filepath)
# .crop((0, 245, 750, 1115)).convert('L')
# img.save('file/3.png')


width = img.size[0]
height = img.size[1]
xy = (width / 2, height / 2)
point = img.getpixel(xy)
print point
print pytesseract.image_to_string(img)
# for i in xrange(0, width):
#     for j in xrange(0, height):
#         print img.getpixel((i, j))

# im = ImageGrab.grab().convert('L')  # 截取全屏
# im.save('file/2.png')
