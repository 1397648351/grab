# -*-coding:utf-8-*-

import sys

from lib.novel import Novel
from lib.grab2 import Grab2
from lib.pictures import Pictures
from lib.grab import Grab
from lib.xmlanalysis import XmlAnalysis
from lib.novel2 import Novel2
import pyttsx

reload(sys)
sys.setdefaultencoding("utf-8")

if __name__ == "__main__":
    engine = pyttsx.init()
    engine.say('开始')
    engine.runAndWait()
    ss = Novel2()
    ss.get_chapters()
    engine.say('结束')
    engine.runAndWait()
# novel = Novel()
# novel.get_chapter()
# pic = Pictures()
# pic.get_page_url()
# Grab2.open_content('https://www.xiashu.la/146539/')

# XmlAnalysis.create_xml('file/t.xml', ele)
