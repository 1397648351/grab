# -*-coding:utf-8-*-

import sys

from lib.novel import Novel
from lib.pictures import Pictures

reload(sys)
sys.setdefaultencoding("utf-8")

if __name__ == "__main__":
    #novel = Novel()
    #novel.get_chapter()
    pic = Pictures()
    pic.get_page_url()
