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
    Search_ID = 0
    Search_Name = 1
    Normal = 0
    ReDownload = 1
    Chrome = 0
    FireFox = 1

    @staticmethod
    def ele_click(driver):
        element = driver.find_element_by_id("yc")
        element.click()
        element = driver.find_element_by_id("zkzj")
        while element.text != '点击关闭':
            time.sleep(0.1)

    def __init__(self, book, mode=Search_ID, download_mode=Normal):
        self.version = '1.0'
        self.mutex = threading.Lock()
        self.coexist = 5
        self.driverName = self.Chrome
        self.driver = None
        self.type = download_mode
        self.url_page = ''
        self.bookid = ''
        self.bookname = ''
        self.introduction = ''
        self.settings = {
            'home': 'https://www.xiashu.la',
            'book': {
                'input': 'shuming',
                'submit': 'submitbtn',
                'link': '#waterfall .item.masonry-brick',
                'link_replace': '/api/ajax/searchid.php?id='
            },
            'page': {
                'rm_eles': ['#aboutbook a.fr', '#aboutbook h3'],
                'do': self.ele_click,
                'name': '#info .infotitle h1',
                'introduction': '#aboutbook',
                'creator': '.ainfo .username a',
                'cover': '#picbox .img_in img',
                'chapters': '#detaillist ul li'
            },
            'chapter': {
                'rm_eles': [],
                'content': '#chaptercontent'
            },
        }
        self.creator = ""
        self.path = 'file/novel'
        self.info = ''
        self.book = {}
        self.chapters = []
        self.str_replace = [
            '一秒记住【棉花糖小说网mianhuatang.la】，为您提供精彩小说阅读。',
            '一秒记住【谷♂粒÷小÷说→网 xinguli】，更新快，无弹窗，免费读！',
            '一秒记住【谷♂粒÷网 xinguli】，精彩小说无弹窗免费阅读！',
            'c_t;', 'reads;', '（ 广告）', '( $&gt;&gt;&gt;棉、花‘糖’小‘說’)',
            '( $>>>棉、花‘糖’小‘說’)', '( )', '（ ）', '[ ]', '（ 棉花糖', '( ’)',
            '[看本书最新章节请到]', '[更新快，网站页面清爽，广告少，，最喜欢这种网站了，一定要好评]',
            '其c他都5是w盗版0`', '天才壹秒記住愛♂去÷小說→網，為您提供精彩小說閱讀。',
            '~搜搜篮色，即可全文阅读后面章节', '-79-', '-79xs-', '&amp;nnsp;',
            '最新章节全文阅读。更多最新章节访问:ww 。', '。 更新好快。',
            '最新章节全文阅读', '。更多最新章节访问:ww 。', 'ＷｗΔＷ．『ksnhuge『ge．La',
            '[想看的书几乎都有啊，比一般的站要稳定很多更新还快，全文字的没有广告。]',
            '恋上你看书网 630bookla ，最快更新神豪无极限最新章节！'
        ]
        if mode == self.Search_ID:
            self.bookid = book
            self.url_page = '%s/%s/' % (self.settings['home'], self.bookid)
            self.get_chapters()
        else:
            self.get_book(book)

    def get_book(self, bookname):
        if self.driverName == self.Chrome:
            self.driver = webdriver.Chrome()
        elif self.driverName == self.FireFox:
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.Chrome()
        try:
            self.driver.get(self.settings['home'])
            input = self.driver.find_element_by_id(self.settings['book']['input'])
            input.send_keys(bookname)
            submit = self.driver.find_element_by_id(self.settings['book']['submit'])
            submit.click()
            html = self.driver.page_source.decode('utf-8', 'ignore')
            html = html.replace('xmlns="http://www.w3.org/1999/xhtml" /', '').replace(
                'xmlns="http://www.w3.org/1999/xhtml"', '')
            doc = pq(html)
            link = doc(self.settings['book']['link'])
            if len(link) > 0:
                link = link.eq(0).find('.title h3 a')
                self.bookname = link.text().strip()
                if bookname != self.bookname:
                    self.driver.quit()
                    print u'未找到该书籍《%s》' % bookname
                    return
                self.bookid = link.attr('href').replace(self.settings['book']['link_replace'], '')
                self.url_page = '%s/%s/' % (self.settings['home'], self.bookid)
                self.get_chapters()
        except Exception, ex:
            self.driver.quit()
            print 'error!', '\n', str(ex)
            return

    def get_chapters(self, url=None):
        if not url:
            url = self.url_page
        if not self.driver:
            if self.driverName == self.Chrome:
                self.driver = webdriver.Chrome()
            elif self.driverName == self.FireFox:
                self.driver = webdriver.Firefox()
            else:
                self.driver = webdriver.Chrome()
        try:
            self.driver.get(url)
            if self.settings['page']['do']:
                self.settings['page']['do'](self.driver)
            # element = self.driver.find_element_by_id("yc")
            # element.click()
            # element = self.driver.find_element_by_id("zkzj")
            # while element.text != '点击关闭':
            #     time.sleep(0.1)
            html = self.driver.page_source.decode('utf-8', 'ignore')
            html = html.replace('xmlns="http://www.w3.org/1999/xhtml" /', '').replace(
                'xmlns="http://www.w3.org/1999/xhtml"', '')
        except Exception, ex:
            print 'error!', '\n', str(ex)
            return
        finally:
            self.driver.quit()
        self.get_bookinfo(html)
        self.create_thread()
        self.save_files()

    def get_bookinfo(self, html):
        doc = pq(html)
        if self.settings['page']['rm_eles']:
            for cur in self.settings['page']['rm_eles']:
                doc(cur).remove()
        introduction = doc(self.settings['page']['introduction']).html()
        self.bookname = doc(self.settings['page']['name']).text().replace(u'《', '').replace(u'》', '').strip()
        self.creator = doc(self.settings['page']['creator']).text().strip()
        if not self.bookname:
            raise Exception('抓取网页失败！')
        self.str_replace.append('恋上你看书网 630bookla ，最快更新%s最新章节！' % self.bookname)
        print "《%s》开始抓取" % self.bookname
        self.create_path()
        list = introduction.split('<br/>')
        for item in list:
            if not item:
                continue
            item = item.strip()
            if not item:
                continue
            self.introduction += item + '<br/>'
        cover = doc(self.settings['page']['cover']).attr('src')
        Grab.download_image(cover, '%s/%s' % (self.path, self.bookname), 'cover')
        list_chapter = doc(self.settings['page']['chapters']).items()
        index = 0
        for chapter in list_chapter:
            title = chapter('a').text()
            href = chapter('a').attr('href')
            if not title or not href:
                continue
            index = index + 1
            self.chapters.append({
                'index': index,
                'title': title,
                'href': href
            })

    def create_path(self):
        folder = os.path.exists('%s/%s.epub' % (self.path, self.bookname))
        if self.type == self.ReDownload:
            if folder:
                os.remove('%s/%s.epub' % (self.path, self.bookname))
                folder = False
            if os.path.exists('%s/%s' % (self.path, self.bookname)):
                shutil.rmtree('%s/%s' % (self.path, self.bookname))
        if folder:
            if not os.path.exists('%s/%s' % (self.path, self.bookname)):
                shutil.copy('%s/%s.epub' % (self.path, self.bookname), '%s/temp.epub' % self.path)
                with zipfile.ZipFile('%s/temp.epub' % self.path) as file:
                    file.extractall('%s/%s' % (self.path, self.bookname))
                    os.remove(os.path.join(self.path, self.bookname, 'mimetype'))
                os.remove('%s/temp.epub' % self.path)
        folder = os.path.exists('%s/%s' % (self.path, self.bookname))
        if not folder:
            os.makedirs('%s/%s' % (self.path, self.bookname))
        folder = os.path.exists('%s/%s/META-INF' % (self.path, self.bookname))
        if not folder:
            os.makedirs('%s/%s/META-INF' % (self.path, self.bookname))
        shutil.copyfile("epub/container.xml", "%s/%s/META-INF/container.xml" % (self.path, self.bookname))
        shutil.copyfile("epub/stylesheet.css", "%s/%s/stylesheet.css" % (self.path, self.bookname))

    def get_chapter_content(self, index, url=None):
        if url is None:
            url = self.url_page
        try:
            file_name = '%05d' % (index + 1)
            file_name = 'chapter_' + file_name + '.xhtml'
            folder = os.path.exists('%s/%s/%s' % (self.path, self.bookname, file_name))
            if folder:
                self.mutex.acquire()
                print '%s %s 已存在！' % (self.bookname, self.chapters[index]["title"])
                self.mutex.release()
                return
            html = Grab.get_content(self.settings['home'] + url).decode("utf-8", 'ignore')
        except Exception, e:
            self.mutex.acquire()
            print url + e.message
            self.mutex.release()
            time.sleep(1)
            self.get_chapter_content(index, url)
            return
        html = html.replace('xmlns="http://www.w3.org/1999/xhtml" /', '').replace(
            'xmlns="http://www.w3.org/1999/xhtml"', '')
        doc = pq(html)
        if self.settings['chapter']['rm_eles']:
            for cur in self.settings['chapter']['rm_eles']:
                doc(cur).remove()
        self.create_chapter(index, doc(self.settings['chapter']['content']).html())

    def create_thread(self):
        threads = []
        for chapter in self.chapters:
            th = threading.Thread(target=self.get_chapter_content, args=(chapter['index'] - 1, chapter['href'],))
            th.start()
            threads.append(th)
            if len(threads) >= self.coexist:
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
        file_name = '%s/%s/catalog.xhtml' % (self.path, self.bookname)
        with open('epub/temp_catalog.xhtml', 'r') as f:
            content = f.read().replace('__CONTENT__', content)
        with open(file_name, 'w') as f:
            f.write(content)
        file_name = '%s/%s/toc.ncx' % (self.path, self.bookname)
        with open('epub/temp_toc.ncx', 'r') as f:
            content_toc = f.read().replace('__CONTENT__', content_toc).replace('__TIME__', id).replace(
                '__CREATOR__', self.creator).replace('__BOOKNAME__', self.bookname)
        with open(file_name, 'w') as f:
            f.write(content_toc)
        file_name = '%s/%s/content.opf' % (self.path, self.bookname)
        with open('epub/temp_content.opf', 'r') as f:
            content_opf = f.read()
            content_opf = content_opf.replace('__BOOKNAME__', self.bookname).replace('__CREATOR__',
                                                                                     self.creator).replace(
                '__TIME__', id).replace('__CONTENT1__', content_opf_1).replace('__CONTENT2__', content_opf_2)
        with open(file_name, 'w') as f:
            f.write(content_opf)

    def create_page(self):
        with open('epub/temp_page.xhtml', 'r') as f:
            content = f.read()
        content = content.replace('__BOOKNAME__', self.bookname).replace(
            '__INTRODUCTION__', self.introduction).replace('__CREATOR__', self.creator)
        file_name = '%s/%s/page.xhtml' % (self.path, self.bookname)
        with open(file_name, 'w') as f:
            f.write(content)

    def create_chapter(self, index, content):
        file_name = '%05d' % (index + 1)
        file_name = 'chapter_' + file_name + '.xhtml'
        folder = os.path.exists('%s/%s/%s' % (self.path, self.bookname, file_name))
        if folder:
            return
        content = content.replace(self.chapters[index]['title'], '').replace(
            self.chapters[index]['title'].replace(' ', ''), '')
        for item in self.str_replace:
            content = content.replace(item, '')
        list = content.split('<br/>')
        contents = ''
        for item in list:
            if not item:
                continue
            item = item.strip()
            if not item:
                continue
            contents += '<p>' + item + '</p>'
        with open('epub/temp_chapter.xhtml', 'r') as f:
            contents = f.read().replace('__CONTENT__', contents).replace('__TITLE__', self.chapters[index]['title'])
        with open('%s/%s/%s' % (self.path, self.bookname, file_name), 'w') as f:
            f.write(contents)
        self.mutex.acquire()
        print self.bookname, '%d/%d' % (index + 1, len(self.chapters)), self.chapters[index]["title"]
        self.mutex.release()

    def save_epub(self):
        folder = os.path.exists('%s/%s.epub' % (self.path, self.bookname))
        if folder:
            os.remove('%s/%s.epub' % (self.path, self.bookname))
        shutil.make_archive('%s/%s' % (self.path, self.bookname), 'zip', '%s/%s' % (self.path, self.bookname))
        os.rename('%s/%s.zip' % (self.path, self.bookname), '%s/%s.epub' % (self.path, self.bookname))
        with zipfile.ZipFile('%s/%s.epub' % (self.path, self.bookname), 'a') as file:
            file.write('epub/mimetype', 'mimetype')
        shutil.rmtree('%s/%s' % (self.path, self.bookname))  # 递归删除文件夹
        print self.bookname + '.epub 完成'
