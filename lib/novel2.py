# -*- coding: utf-8 -*-

import sys
import os
import time
import threading
import shutil
from selenium import webdriver
from pyquery import PyQuery as pq

from lib.grab import Grab

reload(sys)
sys.setdefaultencoding('utf-8')


class Novel2:
    def __init__(self):
        self.version = '1.0'
        self.driver = webdriver.Firefox()
        self.mutex = threading.Lock()

        self.domain = 'https://www.xiashu.la'
        self.url_page = 'https://www.xiashu.la/191565/'
        self.bookname = u'都市奇门医圣'
        self.chapters = []

    def get_chapter_content(self, index, url=None):
        if url is None:
            url = self.url_page
        try:
            html = Grab.get_content(self.domain + url).decode("utf-8", 'ignore')
        except Exception, e:
            print url + e.message
            time.sleep(1)
            self.get_chapter_content(index, url)
            return
        print self.chapters[index]["title"]
        doc = pq(html)
        self.chapters[index]["content"] = doc('#chaptercontent').html()

    def get_chapters(self, url=None):
        try:
            if not url:
                url = self.url_page
            self.driver.get(url)
            element = self.driver.find_element_by_id("yc")
            element.click()
            element = self.driver.find_element_by_id("zkzj")
            while element.text != '点击关闭':
                time.sleep(0.1)
            html = self.driver.page_source.decode('utf-8', 'ignore')
            doc = pq(html)
            list_chapter = doc('#detaillist ul li').items()
            index = 0
            for chapter in list_chapter:
                index = index + 1
                title = chapter('a').text()
                href = chapter('a').attr('href')
                self.chapters.append({
                    'index': index,
                    'title': title,
                    'href': href
                })
            self.create_thread()
            for chapter in self.chapters:
                print chapter['title']
        finally:
            self.driver.close()

    def create_thread(self):
        threads = []
        for chapter in self.chapters:
            th = threading.Thread(target=self.get_chapter_content, args=(chapter['index'] - 1, chapter['href'],))
            th.start()
            threads.append(th)
            if len(threads) >= 5:
                for _th in threads:
                    _th.join()
                del threads[:]
        for _th in threads:
            _th.join()
        del threads[:]

    def save_files(self):
        print 'start'
