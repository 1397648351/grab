# -*-coding:UTF-8-*-
import sys
import threading, time
from lib.grab import Grab
from pyquery import PyQuery

reload(sys)
sys.setdefaultencoding('utf-8')


class Pictures:
    def __init__(self):
        self.mutex = threading.Lock()
        self.url = ""
        self.path = 'file/img'

    def get_page(self, url=None):
        if url is None:
            url = self.url
        try:
            html = Grab.get_content(url).decode('utf-8', 'ignore')
        except Exception, ex:
            print url, ex.message
            self.get_page(url)
