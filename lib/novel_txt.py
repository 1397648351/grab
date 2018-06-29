# -*-coding:utf-8-*-

import sys
import threading, time, re
from lib.grab import Grab
from pyquery import PyQuery as pq

reload(sys)
sys.setdefaultencoding("utf-8")


class Novel:
    def __init__(self):
        self.domain = 'https://www.xiashu.la'
        self.url_catalog = 'https://www.xiashu.la/48758/'
        self.url_page = '/48758/read_1933.html'
        self.novel_name = u'修真聊天群'
        self.catalog = []
        self.mutex = threading.Lock()

    def get_chapter(self, url=None):
        if url is None:
            url = self.url_page
        try:
            html = Grab.get_content(self.domain + url).decode("utf-8", 'ignore')
        except Exception, e:
            print url + e.message
            time.sleep(1)
            self.get_chapter()
            return
        doc = pq(html)
        title = doc('.title h1 a').text().replace(self.novel_name, '').strip()
        chapter = doc('#chaptercontent').text()
        self.write_txt(title, chapter)
        ele_next = doc('.last a')
        if ele_next.attr('title') != u'没有了':
            self.url_page = doc('.last a').attr('href')
            self.get_chapter(self.url_page)

    def write_txt(self, title, content):
        self.mutex.acquire()
        with open('file/' + self.novel_name + ".txt", "a") as f:
            pattern = re.compile(r'.*/read_(.*)\.html', re.M | re.I)
            m = pattern.match(self.url_page)
            page = ''
            if m:
                page = m.group(1)
            title = '第%s章 %s' % (page, title)
            f.write(title + '\n\r')
            f.write(content + '\n\r')
        print title
        self.mutex.release()
