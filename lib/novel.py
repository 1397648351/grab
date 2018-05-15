# -*-coding:utf-8-*-

import sys
import threading, time, re
from lib.grab import Grab
from pyquery import PyQuery as pq

reload(sys)
sys.setdefaultencoding("utf-8")


class Novel:
    def __init__(self):
        self.url_catalog = 'http://www.80txt.com/txtml_695.html'
        self.novel_name = u'叱咤风云'
        self.catalog = []

    def get_catalog(self):
        html = Grab.get_content(self.url_catalog).decode("utf-8")
        print html
        doc = pq(html)
        ele_catalog = doc('#content')
        print ele_catalog.text()
        # for item in ele_catalog:
        #     print item
