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
        self.url_catalog = 'https://www.xiashu.la/12526/'
        self.url_page = '/65423/read_1929.html'
        self.novel_name = u'极品异能学生'
        self.catalog = []
        self.mutex = threading.Lock()

    def get_chapter(self):
        try:
            html = Grab.get_content(self.domain + self.url_page).decode("utf-8", 'ignore')
        except Exception, e:
            print self.url_page + e.message
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
            self.get_chapter()
        # for item in ele_catalog:
        #     print item

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
