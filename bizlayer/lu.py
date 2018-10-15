# -*- coding: utf-8 -*-

import sys
import os
import threading
from pyquery import PyQuery as pq
from lib.grab import Grab

reload(sys)
sys.setdefaultencoding('utf-8')


class Lu:
    YAZHOU = 1
    ZHIFU = 2

    def __init__(self, type, start, end):
        self.version = '1.0'
        self.homepage = 'http://111av.org'
        self.start = start
        self.end = end
        self.type = type
        self.path = 'file/%d' % self.type
        self.mutex = threading.RLock()  # 创建锁

    def create_path(self):
        self.mutex.acquire()
        folder = os.path.exists(self.path)
        if not folder:
            os.makedirs(self.path)
        self.mutex.release()

    def getpages(self):
        for i in xrange(self.start, self.end + 1):
            if i == 1:
                url = "%s/list/%d.html" % (self.homepage, self.type)
            else:
                url = "%s/list/%d-%d.html" % (self.homepage, self.type, i)
            self.create_path()
            self.getpage(url)

    def getpage(self, url):
        thradList = []
        html = Grab.get_content(url).decode('utf-8', 'ignore')
        html = html.replace('xmlns="http://www.w3.org/1999/xhtml" /', '').replace(
            'xmlns="http://www.w3.org/1999/xhtml"', '')
        doc = pq(html)
        links = doc('ul.mlist>li>a').items()
        for link in links:
            href = link.attr('href')
            # self.downimgs(href)
            th = threading.Thread(target=self.downimgs, args=(href,))
            th.start()
            thradList.append(th)
            if len(thradList) > 10:
                while len(thradList):
                    thradList.pop(0).join()

    def downimgs(self, link):
        thradList = []
        url = self.homepage + link
        html = Grab.get_content(url).decode('utf-8', 'ignore')
        html = html.replace('xmlns="http://www.w3.org/1999/xhtml" /', '').replace(
            'xmlns="http://www.w3.org/1999/xhtml"', '')
        doc = pq(html)
        id = link.replace('/vod/', '').replace('.html', '')
        name = doc('.downlist>ul>li>p').text()
        downurl = doc('.downlist>ul>li>span>a.d1').attr('href')
        images = doc('.vodimg>p>img').items()
        path = '%s/%s' % (self.path, id)
        self.mutex.acquire()
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
        if name is not None and downurl is not None:
            with open('%s/%s.txt' % (path, name), 'wb') as f:
                f.write(downurl)
        self.mutex.release()
        i = 0
        for image in images:
            i = i + 1
            src = 'http:' + image.attr('src')
            # Grab.download_image(src, path, '%02d' % i)
            th = threading.Thread(target=Grab.download_image, args=(src, path, '%02d' % i, True,))
            th.start()
            thradList.append(th)
        while len(thradList) > 0:
            thradList.pop(0).join()
        print '%s %s 完成！' % (id, name)
