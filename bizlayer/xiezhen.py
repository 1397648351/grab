# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, re, threading
from lib.grab import Grab
from pyquery import PyQuery as pq

reload(sys)
sys.setdefaultencoding('utf-8')


class Xiezhen:
    kinds = {
        'xinggan': 6,
        'qingchun': 1,
        'xiaohua': 2,
        'chemo': 3,
        'qipao': 4,
        'mingxing': 5
    }

    def __init__(self, limit, count=-1, kind='xinggan'):
        self.version = '1.0'
        self.home = 'http://www.mm131.com'
        self.kind = kind
        self.url = '%s/%s/' % (self.home, kind)
        # self.path = sys.path[0]
        syspath = sys.path[0]
        self.path = u'file/images/写真/%s' % kind
        self.path = os.path.abspath(os.path.join(syspath, self.path))
        self.limit = limit
        self.count = count
        self.threads = []
        self.async = 8
        self.mutex = threading.RLock()

    @classmethod
    def start(cls, limit, count=-1, kind='xinggan'):
        xz = Xiezhen(limit, count, kind)
        xz.get_pages()
        # xz.download_page('http://www.mm131.com/xinggan/4384.html', 0)
        # http://www.mm131.com/xinggan/4366.html

    def get_pages(self):
        pages = []
        if self.count != -1:
            self.limit = self.limit - 1
            pages = xrange(self.limit, self.limit + self.count)
        else:
            pages = xrange(self.limit)
        for page in pages:
            url = ''
            if page != 0:
                url = 'list_%d_%d.html' % (self.kinds[self.kind], page + 1)
            self.get_page(self.url + url)
        while len(self.threads) > 0:
            for i, _th in enumerate(self.threads):
                if not _th.isAlive():
                    self.threads.pop(i).join()

    def get_page(self, url):
        try:
            html = Grab.get_content(url).decode('gb2312', 'ignore')
            html = html.replace('xmlns="http://www.w3.org/1999/xhtml" /', '').replace(
                'xmlns="http://www.w3.org/1999/xhtml"', '')
            doc = pq(html)
            pages = doc('.main .list-left dd[class!=page]').items()
            for page in pages:
                href = page('a').attr('href')
                th = threading.Thread(target=self.download_page, args=(href, 0,))
                th.start()
                self.threads.append(th)
                while len(self.threads) >= self.async:
                    for i, _th in enumerate(self.threads):
                        if not _th.isAlive():
                            self.threads.pop(i).join()
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
        Grab.download_image(imgsrc, path, '%03d' % index, noprint=False, headers_referer='http://www.mm131.com')
        next = doc('.content-page a:last')
        if next.text() != '下一页':
            next = False
        if next:
            url = next.attr('href')
            index = re.match(r'.*_([0-9]+).html', url)
            if index:
                index = int(index.group(1))
                self.download_page(self.url + url, index)
