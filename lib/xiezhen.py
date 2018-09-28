# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, re, threading
from grab import Grab
from pyquery import PyQuery as pq

reload(sys)
sys.setdefaultencoding('utf-8')


class Xiezhen:
    def __init__(self, limit, count=-1):
        self.version = '1.0'
        self.url = 'http://www.mm131.com/xinggan/'
        # self.path = sys.path[0]
        syspath = sys.path[0]
        self.path = 'file/images/xingan'
        self.path = os.path.abspath(os.path.join(syspath, self.path))
        self.limit = limit
        self.count = count
        self.mutex = threading.RLock()

    @classmethod
    def start(cls, limit, count=-1):
        xz = Xiezhen(limit, count)
        # xz.get_pages()
        xz.download_page('http://www.mm131.com/xinggan/4366.html', 0)
        # http://www.mm131.com/xinggan/4366.html

    def get_pages(self):
        url = self.url
        if self.limit != 0 and self.count != -1:
            pass
        try:
            html = Grab.get_content(url).decode('gb2312', 'ignore')
            html = html.replace('xmlns="http://www.w3.org/1999/xhtml" /', '').replace(
                'xmlns="http://www.w3.org/1999/xhtml"', '')
            doc = pq(html)
            pages = doc('.main .list-left dd[class!=page]').items()
            for page in pages:
                print page('a').text()
        except Exception, e:
            print str(e)

    def download_page(self, url, index=0):
        self.mutex.acquire()
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.mutex.release()
        try:
            html = Grab.get_content(url).decode('gb2312', 'ignore')
        except Exception, e:
            print str(e)
            self.download_page(url, index)
            return
        html = html.replace('xmlns="http://www.w3.org/1999/xhtml" /', '').replace(
            'xmlns="http://www.w3.org/1999/xhtml"', '')
        doc = pq(html)
        title = doc('.content h5').text()
        title = re.sub(r'\([0-9]*\)', '', title)
        path = os.path.join(self.path, title)
        self.mutex.acquire()
        if not os.path.exists(path):
            os.mkdir(path)
        self.mutex.release()
        imgsrc = doc('.content .content-pic a img').attr('src')
        Grab.download_image(imgsrc, path, '%03d' % index, headers_referer='http://www.mm131.com')
        next = doc('.content-page a:last')
        if next.text() != '下一页':
            next = False
        if next:
            url = next.attr('href')
            index = re.match(r'.*_([0-9]*).html', url)
            if index:
                index = int(index.group(1))
                self.download_page(self.url + url, index)
