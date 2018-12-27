# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time   : 2018/12/27 23:13
# @Author : WuZe
# @Desc   :
# ==================================================

import sys, os, re, time, threading
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

    def __init__(self, limit, to=0, kind='xinggan'):
        self.version = '1.0'
        self.home = 'http://www.mm131.com'
        self.kind = kind
        self.url = '%s/%s/' % (self.home, kind)
        # self.path = sys.path[0]
        syspath = sys.path[0]
        self.path = u'file/images/写真/%s' % kind
        self.path = os.path.abspath(os.path.join(syspath, self.path))
        self.limit = limit
        self.to = to
        self.items = []
        self.threads = []
        self.total = 0
        self.index = 0
        self.async = 8
        self.mutex = threading.RLock()
        self.run = True

    def start(self):
        print u'正在获取图片资源...'
        self.get_pages()
        print u'共计%d项，%d张。' % (len(self.items), self.total)
        print u'开始下载....'
        self.download_items()
        self.run = False

    def stop(self):
        self.run = False

    def get_pages(self):
        pages = []
        threads = []
        if self.to != 0:
            pages = xrange(self.limit - 1, self.to)
        else:
            pages = xrange(self.limit)
        for page in pages:
            if not self.run:
                break
            url = ''
            if page != 0:
                url = 'list_%d_%d.html' % (self.kinds[self.kind], page + 1)
            th = threading.Thread(target=self.get_page_items, args=(self.url + url,))
            th.start()
            threads.append(th)
            # self.get_page_items(self.url + url)
            while len(threads) >= self.async / 2:
                for i, _th in enumerate(threads):
                    if not _th.isAlive():
                        threads.pop(i).join()
        self.threads = self.threads + threads
        while len(self.threads) > 0:
            for i, _th in enumerate(self.threads):
                if not _th.isAlive():
                    self.threads.pop(i).join()

    def get_page_items(self, url):
        try:
            html = Grab.get_content(url).decode('gb2312', 'ignore')
        except Exception, e:
            print '\r' + str(e), url,
            sys.stdout.flush()
            if self.run:
                time.sleep(.1)
                self.get_page(url)
                return
        html = html.replace('xmlns="http://www.w3.org/1999/xhtml" /', '').replace(
            'xmlns="http://www.w3.org/1999/xhtml"', '')
        doc = pq(html)
        items = doc('.main .list-left dd[class!=page]').items()
        threads = []
        for item in items:
            if not self.run:
                break
            href = item('a').attr('href')
            th = threading.Thread(target=self.get_item_info, args=(href,))
            th.start()
            threads.append(th)
            while len(threads) >= self.async / 2:
                for i, _th in enumerate(threads):
                    if not _th.isAlive():
                        threads.pop(i).join()
        self.threads = self.threads + threads

    def get_item_info(self, url):
        try:
            html = Grab.get_content(url).decode('gb2312', 'ignore')
        except Exception, e:
            print '\r' + str(e), url,
            sys.stdout.flush()
            if self.run:
                time.sleep(.1)
                self.get_item_info(url)
                return
        html = html.replace('xmlns="http://www.w3.org/1999/xhtml" /', '').replace(
            'xmlns="http://www.w3.org/1999/xhtml"', '')
        doc = pq(html)
        info = {
            'id': '',
            'title': doc('.content h5').text().strip(),
            'count': 0
        }
        matchObj = re.match(r'%s([0-9]+)(_[0-9]+)?.html' % self.url, url)
        if matchObj:
            info['id'] = matchObj.group(1)
        count = doc('.content-page span:first').text().strip()
        matchObj = re.match(ur'共([0-9]+)页', count)
        if matchObj:
            info['count'] = int(matchObj.group(1))
        self.mutex.acquire()
        self.items.append(info)
        self.total += info['count']
        self.mutex.release()

    def down_img(self, index):
        # http://img1.mm131.me/pic/4190/36.jpg
        self.mutex.acquire()
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.mutex.release()

    def download_items(self):
        for index, item in enumerate(self.items):
            if not self.run:
                break
            for i in xrange(item['count']):
                if not self.run:
                    break
                th = threading.Thread(target=self.download_img, args=(index, i + 1,))
                th.start()
                self.threads.append(th)
                while len(self.threads) >= self.async:
                    for j, _th in enumerate(self.threads):
                        if not _th.isAlive():
                            self.threads.pop(j).join()
        while len(self.threads) > 0:
            for i, _th in enumerate(self.threads):
                if not _th.isAlive():
                    self.threads.pop(i).join()

    def download_img(self, index, i):
        path = os.path.join(self.path, '%s%s' % (self.items[index]['id'].zfill(5), self.items[index]['title']))
        self.mutex.acquire()
        if not os.path.exists(path):
            os.makedirs(path)
        self.mutex.release()
        src = 'http://img1.mm131.me/pic/%s/%d.jpg' % (self.items[index]['id'], i)
        try:
            Grab.download_image(src, path, '%03d' % i, noprint=True, headers_referer='http://www.mm131.com')
            self.mutex.acquire()
            self.index += 1
            percent = self.index * 100.0 / self.total
            print '\r%.2f%%' % percent,
            sys.stdout.flush()
            self.mutex.release()
        except Exception:
            if self.run:
                time.sleep(.1)
                self.download_img(index, i)
