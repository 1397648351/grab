# -*-coding:utf-8-*-

import sys

from lib.novel import Novel
from lib.pictures import Pictures
from lib.grab2 import Grab2
from lib.grab import Grab
# from pyquery import PyQuery as pq
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")

if __name__ == "__main__":
    # novel = Novel()
    # novel.get_chapter()
    # pic = Pictures()
    # pic.get_page_url()
    Grab2.open_content('https://www.xiashu.la/146539/')
