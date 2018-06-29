# -*- coding: utf-8 -*-

import sys
import os
import time
import threading
import shutil
from selenium import webdriver
from pyquery import PyQuery as pq
import zipfile

from lib.grab import Grab

reload(sys)
sys.setdefaultencoding('utf-8')


class Novel:
    def __init__(self):
        self.version = '1.0'
        self.mutex = threading.Lock()

        self.bookid = "146539"
        self.domain = 'https://www.xiashu.la'
        self.url_page = 'https://www.xiashu.la/%s/' % self.bookid
        self.bookname = ''
        self.introduction = ""
        self.path = ''
        self.info = ''
        self.book = {}
        self.chapters = []
        self.str_replace = []

    def get_chapters(self, url=None):
        if not url:
            url = self.url_page
        driver = webdriver.Chrome()
        try:
            driver.get(url)
            element = driver.find_element_by_id("yc")
            element.click()
            element = driver.find_element_by_id("zkzj")
            while element.text != '点击关闭':
                time.sleep(0.1)
            html = driver.page_source.decode('utf-8', 'ignore')
            html = html.replace('xmlns="http://www.w3.org/1999/xhtml"', '')
        except Exception, ex:
            print 'error!', '\n', str(ex)
            return
        finally:
            driver.quit()
        doc = pq(html)
        doc('#aboutbook a.fr').remove()
        doc('#aboutbook h3').remove()
        introduction = doc('#aboutbook').html()
        self.bookname = doc('#info .infotitle h1').text().replace(u'《', '').replace(u'》', '').strip()
        if not self.bookname:
            raise Exception('抓取网页失败！')
        self.path = 'file/' + self.bookname
        print "《%s》开始抓取" % self.bookname
        self.create_path()
        list = introduction.split('<br/>')
        for item in list:
            if not item:
                continue
            self.introduction = self.introduction + '<li>' + item.strip() + '</li>'
        cover = doc('#picbox .img_in img').attr('src')
        Grab.download_image(cover, self.path, 'cover')
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
        self.save_files()

    def create_path(self):
        folder = os.path.exists('file/%s.epub' % self.bookname)
        if folder:
            if not os.path.exists(self.path):
                shutil.copy('file/%s.epub' % self.bookname, 'file/temp.epub')
                with zipfile.ZipFile('file/temp.epub') as file:
                    file.extractall(self.path)
                    os.remove(os.path.join(self.path, 'mimetype'))
                os.remove('file/temp.epub')
        folder = os.path.exists(self.path)
        if not folder:
            os.makedirs(self.path)
        folder = os.path.exists(self.path + '/META-INF')
        if not folder:
            os.makedirs(self.path + '/META-INF')
        shutil.copyfile("epub/container.xml", self.path + "/META-INF/container.xml")
        shutil.copyfile("epub/stylesheet.css", self.path + "/stylesheet.css")

    def get_chapter_content(self, index, url=None):
        if url is None:
            url = self.url_page
        try:
            file_name = '%05d' % (index + 1)
            file_name = 'chapter_' + file_name + '.xhtml'
            folder = os.path.exists(self.path + '/' + file_name)
            if folder:
                self.mutex.acquire()
                print self.chapters[index]["title"] + '  已存在！'
                self.mutex.release()
                return
            self.mutex.acquire()
            html = Grab.get_content(self.domain + url).decode("utf-8", 'ignore')
            self.mutex.release()
        except Exception, e:
            self.mutex.acquire()
            print url + e.message
            self.mutex.release()
            time.sleep(1)
            self.get_chapter_content(index, url)
            return
        self.mutex.acquire()
        print self.chapters[index]["title"]
        self.mutex.release()
        html = html.replace('xmlns="http://www.w3.org/1999/xhtml"', '')
        doc = pq(html)
        self.create_chapter(index, doc('#chaptercontent').html())

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
        self.create_page()
        self.create_catalog()
        self.save_epub()

    def create_catalog(self):
        id = str(int(time.time()))
        content = ''
        content_toc = ''
        content_opf_1 = ''
        content_opf_2 = ''
        for chapter in self.chapters:
            _name = '%05d' % chapter['index']
            name = 'chapter_' + _name
            content = content + '<li class="catalog"><a href="' + name + '.xhtml">' + chapter['title'] + '</a></li>'
            content_toc = content_toc + '<navPoint id="' + name + '" playOrder="' + str(chapter['index']) + '">'
            content_toc = content_toc + '<navLabel><text>' + chapter['title'] + '</text></navLabel>'
            content_toc = content_toc + '<content src="' + name + '.xhtml"/></navPoint>'
            content_opf_1 = content_opf_1 + '<item href="' + name + '.xhtml" id="id' + _name + '" media-type="application/xhtml+xml"/>'
            content_opf_2 = content_opf_2 + '<itemref idref="id' + _name + '"/>'
        file_name = self.path + '/catalog.xhtml'
        with open('epub/temp_catalog.xhtml', 'r') as f:
            content = f.read().replace('__CONTENT__', content)
        with open(file_name, 'w') as f:
            f.write(content)
        file_name = self.path + '/toc.ncx'
        with open('epub/temp_toc.ncx', 'r') as f:
            content_toc = f.read().replace('__CONTENT__', content_toc).replace('__TIME__', id).replace(
                '__CREATOR__', "WZ").replace('__BOOKNAME__', self.bookname)
        with open(file_name, 'w') as f:
            f.write(content_toc)
        file_name = self.path + '/content.opf'
        with open('epub/temp_content.opf', 'r') as f:
            content_opf = f.read()
            content_opf = content_opf.replace('__BOOKNAME__', self.bookname).replace('__CREATOR__', "WZ").replace(
                '__TIME__', id).replace('__CONTENT1__', content_opf_1).replace('__CONTENT2__', content_opf_2)
        with open(file_name, 'w') as f:
            f.write(content_opf)

    def create_page(self):
        with open('epub/temp_page.xhtml', 'r') as f:
            content = f.read()
        content = content.replace('__BOOKNAME__', self.bookname).replace('__INTRODUCTION__', self.introduction)
        file_name = self.path + '/page.xhtml'
        with open(file_name, 'w') as f:
            f.write(content)

    def create_chapter(self, index, content):
        file_name = '%05d' % (index + 1)
        file_name = 'chapter_' + file_name + '.xhtml'
        folder = os.path.exists(self.path + '/' + file_name)
        if folder:
            return
        for item in self.str_replace:
            content = content.replace(item, '')
        list = content.split('<br/>')
        contents = ''
        for item in list:
            if not item:
                continue
            contents = contents + '<p>' + item.strip() + '</p>'
        with open('epub/temp_chapter.xhtml', 'r') as f:
            contents = f.read().replace('__CONTENT__', contents).replace('__TITLE__', self.chapters[index]['title'])
        with open(self.path + '/' + file_name, 'w') as f:
            f.write(contents)

    def save_epub(self):
        folder = os.path.exists('file/%s.epub' % self.bookname)
        if folder:
            os.remove('file/%s.epub' % self.bookname)
        shutil.make_archive('file/%s' % self.bookname, 'zip', self.path)
        os.rename('file/%s.zip' % self.bookname, 'file/%s.epub' % self.bookname)
        with zipfile.ZipFile('file/%s.epub' % self.bookname, 'a') as file:
            file.write('epub/mimetype', 'mimetype')
        shutil.rmtree(self.path)  # 递归删除文件夹
