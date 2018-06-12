# -*-coding:UTF-8-*-
import sys
import threading
import time
from lib.grab import Grab
from pyquery import PyQuery as pq

reload(sys)
sys.setdefaultencoding('utf-8')


class Pictures:
    def __init__(self):
        self.mutex = threading.Lock()
        self.home = 'http://8888av.vip'
        self.url = "/html/tupian/yazhou/index.html"
        self.path = 'file/img'
        self.re_title = u'亚洲色图 - 千百撸'

    def get_page(self, url=None):
        if url is None:
            url = self.url
        try:
            html = Grab.get_content(url).decode('utf-8', 'ignore')
        except Exception, ex:
            print url, ex.message
            self.get_page(url)
        doc = pq(html)
        title = doc('title').text().replace(self.re_title, '').strip()
        imgs = doc('.artbody.imgbody p img').items()
        i = 0
        for img in imgs:
            i = i + 1
            name = '%03d' % i
            src = 'http:' + img.attr('src')
            path = '%s/%s' % (self.path, title)
            t = threading.Thread(target=self.saveImg, args=(src, path, name,))
            t.start()

    def saveImg(self, url, path, name):
        success = Grab.download_image(url, path, name)
        if success:
            print path, name

    def get_page_url(self, url=None):
        if url is None:
            url = self.home + self.url
        try:
            html = Grab.get_content(url).decode('utf-8', 'ignore')
        except Exception, ex:
            print url, ex.message
            self.get_page_url(url)
        if html is None:
            print 'error:' + url
            return
        doc = pq(html)
        urls = doc('.art ul li a').items()
        threads = []
        for url in urls:
            url = self.home + url.attr('href')
            t = threading.Thread(target=self.get_page, args=(url,))
            t.start()
            threads.append(t)
            if len(threads) > 4:
                for th in threads:
                    th.join()
                del threads[:]
        if len(threads) > 0:
            for th in threads:
                th.join()
