# -*-coding:utf-8-*-

import sys
from pyocr import pyocr
from PIL import Image, ImageGrab

reload(sys)
sys.setdefaultencoding("utf-8")

filepath = 'file/3.png'
img = Image.open(filepath).crop((0, 245, 750, 1115)).convert('L')
#img.save('file/3.png')

xy = (255, 525)
point = img.getpixel(xy)
print point

width = img.size[0]
height = img.size[1]
# for i in xrange(0, width):
#     for j in xrange(0, height):
#         print img.getpixel((i, j))

# im = ImageGrab.grab().convert('L')  # 截取全屏
# im.save('file/2.png')
