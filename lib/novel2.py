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
        self.url_page = 'https://www.xiashu.la/12212/'
        self.bookname = u'黄金瞳'
        self.path = 'file/' + self.bookname
        self.info = ''
        self.book = {}
        self.chapters = []

    def get_chapters(self, url=None):
        if not url:
            url = self.url_page
        self.create_path()
        self.driver.get(url)
        element = self.driver.find_element_by_id("yc")
        element.click()
        element = self.driver.find_element_by_id("zkzj")
        while element.text != '点击关闭':
            time.sleep(0.1)
        html = self.driver.page_source.decode('utf-8', 'ignore')
        self.driver.close()
        doc = pq(html)
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
        folder = os.path.exists(self.path)
        if not folder:
            os.makedirs(self.path)
        folder = os.path.exists(self.path + '/META-INF')
        if not folder:
            os.makedirs(self.path + '/META-INF')
        shutil.copyfile("epub/container.xml", self.path + "/META-INF/container.xml")
        shutil.copyfile("epub/mimetype", self.path + "/mimetype")
        shutil.copyfile("epub/stylesheet.css", self.path + "/stylesheet.css")

    def get_chapter_content(self, index, url=None):
        if url is None:
            url = self.url_page
        try:
            file_name = '%05d' % (index + 1)
            file_name = 'chapter_' + file_name + '.xhtml'
            folder = os.path.exists(self.path + '/' + file_name)
            if folder:
                print self.chapters[index]["title"] + '  已存在！'
                return
            html = Grab.get_content(self.domain + url).decode("utf-8", 'ignore')
        except Exception, e:
            print url + e.message
            time.sleep(1)
            self.get_chapter_content(index, url)
            return
        print self.chapters[index]["title"]
        doc = pq(html)
        self.create_xhtml(index, doc('#chaptercontent').html())

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

    def create_catalog(self):
        id = str(int(time.time()))
        content = '<?xml version="1.0" encoding="utf-8" standalone="no"?>\
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"> \
            <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN">\
            <head><title>目录</title><link href="stylesheet.css" type="text/css" rel="stylesheet"/>\
            <style type="text/css">@page { margin-bottom: 5.000000pt; margin-top: 5.000000pt; }</style></head>\
            <body><h1>目录<br/>Content</h1><ul>'
        content_toc = '<?xml version="1.0" encoding="utf-8"?><ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\
            <head><meta content="' + id + '" name="dtb:uid"/> \
            <meta content="2" name="dtb:depth"/><meta content="0" name="dtb:totalPageCount"/>\
            <meta content="WUZE" name="dtb:generator"/>\
            <meta content="0" name="dtb:maxPageNumber"/></head><docTitle><text>' + self.bookname + '</text></docTitle>\
            <docAuthor><text></text></docAuthor><navMap>'
        content_opf_1 = '<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf"' \
                        ' xmlns:dc="http://purl.org/dc/elements/1.1/" unique-identifier="bookid" version="2.0">\
                      <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">\
                      <dc:title>' + self.bookname + '</dc:title><dc:creator>WUZE</dc:creator>\
                      <dc:date>' + id + '</dc:date><dc:contributor>WUZE</dc:contributor><dc:publisher>WUZE</dc:publisher> \
                      <dc:subject>' + self.bookname + '</dc:subject> \
                      <dc:language>zh-cn</dc:language> \
                      <dc:identifier id = "bookid" >' + id + '</dc:identifier> \
                      <meta name="cover" content="cover-image"/></metadata>\
            <manifest><item href="catalog.xhtml" id="catalog" media-type="application/xhtml+xml"/> \
            <item id="cover-image" href="cover.jpg" media-type="image/jpeg"/>\
            <item href="stylesheet.css" id="css" media-type="text/css"/>\
            <item href="page.xhtml" id="page" media-type="application/xhtml+xml"/>\
            <item href="toc.ncx" media-type="application/x-dtbncx+xml" id="ncx"/>'
        content_opf_2 = '<spine toc="ncx"><itemref idref="page"/><itemref idref="catalog"/>'
        for chapter in self.chapters:
            _name = '%05d' % chapter['index']
            name = 'chapter_' + _name
            content = content + '<li class="catalog"><a href="' + name + '.xhtml">' + chapter['title'] + '</a></li>'
            content_toc = content_toc + '<navPoint id="' + name + '" playOrder="' + str(
                chapter['index']) + '"><navLabel>' \
                                    '<text>' + chapter[
                              'title'] + '</text></navLabel><content src="' + name + '.xhtml"/></navPoint>'
            content_opf_1 = content_opf_1 + '<item href="' + name + '.xhtml" id="id' + _name + '" media-type="application/xhtml+xml"/>'
            content_opf_2 = content_opf_2 + '<itemref idref="id' + _name + '"/>'
        content = content + '</ul><div class="mbppagebreak"></div></body></html>'
        content_toc = content_toc + '</navMap></ncx>'
        content_opf_1 = content_opf_1 + '</manifest>'
        content_opf_2 = content_opf_2 + '</spine><guide><reference href="catalog.xhtml" type="toc" title="目录"/></guide></package>'
        file_name = self.path + '/catalog.xhtml'
        with open(file_name, 'w') as f:
            f.write(content)
        file_name = self.path + '/toc.ncx'
        with open(file_name, 'w') as f:
            f.write(content_toc)
        file_name = self.path + '/content.opf'
        with open(file_name, 'w') as f:
            f.write(content_opf_1 + content_opf_2)

    def create_page(self):
        content = '<?xml version="1.0" encoding="utf-8" standalone="no"?>' \
                  '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">' \
                  '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN">' \
                  '<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>' \
                  '<title>书籍信息</title></head><body><div><h1>' + self.bookname + '</h1></div></body></html>'
        file_name = self.path + '/page.xhtml'
        with open(file_name, 'w') as f:
            f.write(content)

    def create_xhtml(self, index, content):
        file_name = '%05d' % (index + 1)
        file_name = 'chapter_' + file_name + '.xhtml'
        folder = os.path.exists(self.path + '/' + file_name)
        if folder:
            return
        list = content.split('<br/>')
        contents = '<?xml version="1.0" encoding="utf-8" standalone="no"?>\
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"> \
            <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN"> \
            <head><title>' + self.chapters[index]['title'] + '</title><link href="stylesheet.css" type="text/css" rel="stylesheet"/><style type="text/css">\
            @page { margin-bottom: 5.000000pt; margin-top: 5.000000pt; }</style></head><body>\
            <h2><span style="border-bottom:1px solid">' + self.chapters[index]['title'] + '</span></h2>'
        for item in list:
            if not item:
                continue
            contents = contents + '<p>' + item.strip() + '</p>'
        contents = contents + '<div class="mbppagebreak"></div></body></html>'
        with open(self.path + '/' + file_name, 'w') as f:
            f.write(contents)
