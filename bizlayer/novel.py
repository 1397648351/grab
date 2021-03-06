# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time   : 2018/12/27 23:13
# @Author : WuZe
# @Desc   :
# ==================================================

import sys, os, time, re, threading, shutil, zipfile, zlib, json

sys.path.append("..")
import bizlayer.novel_config as config
from selenium import webdriver
from pyquery import PyQuery as pq
from common.spider import Spider


class Novel:
    Search_ID = 0
    Search_Name = 1
    Normal = 0
    ReDownload = 1
    Chrome = 0
    FireFox = 1
    Edge = 2
    Ie = 3

    def __init__(self, book, mode=Search_ID, download_mode=Normal, website=config.biquge, driver_name=Chrome):
        self.version = '1.0'
        self.mutex = threading.Lock()
        self.coexist = 5
        self.num = 0
        self.driverName = driver_name
        self.driver = None
        self.type = download_mode
        self.url_page = ''
        self.bookid = ''
        self.bookname = ''
        self.introduction = ''
        self.settings = config.settings[website]
        self.str_replace = config.str_replace
        if os.path.exists(os.path.join(sys.path[0], 'novel.json')):
            with open(os.path.join(sys.path[0], 'novel.json')) as f:
                # conf = json.loads(f.read().decode('utf-8'))
                conf = json.loads(f.read())
                if 'str_replace' in conf:
                    self.str_replace = self.str_replace + conf['str_replace']
        self.template = os.path.abspath(os.path.join(sys.path[0], 'template/epub'))
        self.creator = ""
        self.path = os.path.abspath(os.path.join(sys.path[0], config.SAVE_PATH))
        self.info = ''
        self.book = {}
        self.chapters = []
        self.strlen = 0
        # self.threads = []
        self.state = False
        if mode == self.Search_ID:
            self.bookid = book
            self.url_page = '%s/%s/' % (self.settings['home'], self.bookid)
            self.get_chapters()
        else:
            self.get_book(book)

    def get_book(self, bookname):
        # if not isinstance(bookname, unicode):
        #     bookname = unicode(bookname, 'utf-8')
        if self.driverName == self.Chrome:
            chrome_opt = webdriver.ChromeOptions()
            prefs = {'profile.managed_default_content_settings.images': 2}
            chrome_opt.add_experimental_option('prefs', prefs)
            self.driver = webdriver.Chrome(chrome_options=chrome_opt)
        elif self.driverName == self.FireFox:
            firefox_profile = webdriver.FirefoxProfile()
            firefox_profile.set_preference('permissions.default.image', 2)
            self.driver = webdriver.Firefox(firefox_profile)
        elif self.driverName == self.Edge:
            self.driver = webdriver.Edge()
        elif self.driverName == self.Ie:
            self.driver = webdriver.Ie()
        else:
            self.driver = webdriver.Chrome()
        try:
            self.driver.get(self.settings['home'])
            input = self.driver.find_element_by_id(self.settings['book']['input'])
            input.send_keys(bookname)
            submit = self.driver.find_element_by_id(self.settings['book']['submit'])
            submit.click()
            # html = self.driver.page_source.decode('utf-8', 'ignore')
            html = self.driver.page_source
            html = html.replace('xmlns="http://www.w3.org/1999/xhtml" /', '').replace(
                'xmlns="http://www.w3.org/1999/xhtml"', '')
            doc = pq(html)
            link = doc(self.settings['book']['link'])
            if len(link) > 0:
                link = link.eq(0).find(self.settings['book']['href'])
                self.bookname = link.text().strip()
                if bookname != self.bookname:
                    self.driver.quit()
                    print('未找到该书籍《%s》' % bookname)
                    return
                self.bookid = link.attr('href').replace(self.settings['book']['link_replace'], '')
                self.url_page = '%s/%s/' % (self.settings['home'], self.bookid)
                self.get_chapters()
        except Exception as ex:
            self.driver.quit()
            print('error!', '\n', str(ex))
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
            html = self.driver.page_source
            # html = html.decode('utf-8', 'ignore')
            html = html.replace('xmlns="http://www.w3.org/1999/xhtml" /', '').replace(
                'xmlns="http://www.w3.org/1999/xhtml"', '')
        except Exception as ex:
            print('error!', '\n', str(ex))
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
        print("《%s》开始抓取" % self.bookname)
        self.create_path()
        _list = introduction.split('<br/>')
        for item in _list:
            if not item:
                continue
            item = item.strip()
            if not item:
                continue
            self.introduction += item + '<br/>'
        cover = doc(self.settings['page']['cover']).attr('src')
        Spider.download_image(cover, os.path.join(self.path, self.bookname), 'cover')
        list_chapter = doc(self.settings['page']['chapters']).items()
        index = 0
        for chapter in list_chapter:
            title = chapter('a').text()
            href = chapter('a').attr('href')
            if not title or not href:
                break  # continue
            index = index + 1
            self.chapters.append({
                'index': index,
                'title': title,
                'href': href
            })

    def create_path(self):
        tempbookpath = os.path.join(self.path, 'temp.epub')
        bookpath = os.path.join(self.path, '%s.epub' % self.bookname)
        bookdirpath = os.path.join(self.path, self.bookname)
        folder = os.path.exists(bookpath)
        if self.type == self.ReDownload:
            if folder:
                os.remove(bookpath)
                folder = False
            if os.path.exists(bookdirpath):
                shutil.rmtree(bookdirpath)
        if folder:
            if not os.path.exists(bookdirpath):
                shutil.copy(bookpath, tempbookpath)
                with zipfile.ZipFile(tempbookpath) as file:
                    file.extractall(bookdirpath)
                    os.remove(os.path.join(self.path, self.bookname, 'mimetype'))
                os.remove(tempbookpath)
        folder = os.path.exists(bookdirpath)
        if not folder:
            os.makedirs(bookdirpath)
        folder = os.path.exists(os.path.join(bookdirpath, 'META-INF'))
        if not folder:
            os.makedirs(os.path.join(bookdirpath, 'META-INF'))
        shutil.copyfile(os.path.join(self.template, 'container.xml'),
                        os.path.join(bookdirpath, 'META-INF', 'container.xml'))
        shutil.copyfile(os.path.join(self.template, 'stylesheet.css'),
                        os.path.join(bookdirpath, 'stylesheet.css'))

    def get_chapter_content(self, index, url):
        _url = url
        try:
            bookdirpath = os.path.join(self.path, self.bookname)
            file_name = '%05d' % (index + 1)
            file_name = 'chapter_' + file_name + '.xhtml'
            folder = os.path.exists(os.path.join(bookdirpath, file_name))
            if folder:
                self.mutex.acquire()
                self.num += 1
                percent = self.num * 100.0 / len(self.chapters)
                _str = '%s [%.2f%%] (%d/%d) %d 已存在！' % (self.bookname, percent, self.num, len(self.chapters), index)
                # _str = '%s [%.2f%%] %s 已存在！' % (self.bookname, percent, self.chapters[index]["title"])
                print('\r%s' % _str, )
                sys.stdout.flush()
                self.mutex.release()
                return
            if self.settings['page']['link_concat']:
                _url = self.settings['home'] + url
            html = Spider.get_content(_url)
            if self.settings['chapter']['gzip']:
                html = zlib.decompress(html, zlib.MAX_WBITS | 16)
            html = html.decode(self.settings['decode'], 'ignore')
        except Exception as e:
            self.mutex.acquire()
            # print '\r%s %s ' % (_url, e.message),
            print('%s %s' % (_url, str(e)))
            sys.stdout.flush()
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
            while len(threads) >= self.coexist:
                for inx, th in enumerate(threads):
                    if not th.isAlive():
                        threads.pop(inx).join()
                # while len(threads) > 0:
        while len(threads) > 0:
            threads.pop(0).join()

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
        bookdirpath = os.path.join(self.path, self.bookname)
        file_name = os.path.join(bookdirpath, 'catalog.xhtml')
        with open(os.path.join(self.template, 'temp_catalog.xhtml'), 'r', encoding='utf-8') as f:
            content = f.read().replace('__CONTENT__', content)
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)
        file_name = os.path.join(bookdirpath, 'toc.ncx')
        with open(os.path.join(self.template, 'temp_toc.ncx'), 'r', encoding='utf-8') as f:
            content_toc = f.read().replace('__CONTENT__', content_toc).replace('__TIME__', id).replace(
                '__CREATOR__', self.creator).replace('__BOOKNAME__', self.bookname)
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content_toc)
        file_name = os.path.join(bookdirpath, 'content.opf')
        with open(os.path.join(self.template, 'temp_content.opf'), 'r', encoding='utf-8') as f:
            content_opf = f.read()
            content_opf = content_opf.replace('__BOOKNAME__', self.bookname).replace('__CREATOR__',
                                                                                     self.creator).replace(
                '__TIME__', id).replace('__CONTENT1__', content_opf_1).replace('__CONTENT2__', content_opf_2)
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content_opf)

    def create_page(self):
        with open(os.path.join(self.template, 'temp_page.xhtml'), 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('__BOOKNAME__', self.bookname).replace(
            '__INTRODUCTION__', self.introduction).replace('__CREATOR__', self.creator)
        bookdirpath = os.path.join(self.path, self.bookname)
        file_name = os.path.join(bookdirpath, 'page.xhtml')
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)

    def create_chapter(self, index, content):
        bookdirpath = os.path.join(self.path, self.bookname)
        file_name = '%05d' % (index + 1)
        file_path = os.path.join(bookdirpath, 'chapter_' + file_name + '.xhtml')
        folder = os.path.exists(file_path)
        if folder:
            return
        # content = content.replace(self.chapters[index]['title'], '').replace(
        #     self.chapters[index]['title'].replace(' ', ''), '')
        _list = content.split('<br/>')
        contents = ''
        for item in _list:
            if not item:
                continue
            item = item.strip()
            if not item:
                continue
            contents += '<p>' + item + '</p>'
        for item in self.str_replace:
            if not isinstance(item, list):
                item = item.replace('__BOOKNAME__', self.bookname)
                contents = contents.replace(item, '')
            else:
                contents, num = re.subn(item[0], item[1], contents, flags=re.M)
        with open(os.path.join(self.template, 'temp_chapter.xhtml'), 'r', encoding='utf-8') as f:
            contents = f.read().replace('__CONTENT__', contents).replace('__TITLE__', self.chapters[index]['title'])
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(contents)
        self.mutex.acquire()
        self.num += 1
        percent = self.num * 100.0 / len(self.chapters)
        _str = '%s [%.2f%%] (%d/%d) %d %s' % (
            self.bookname, percent, self.num, len(self.chapters), index, self.chapters[index]["title"])
        print('\r%s' % _str)
        sys.stdout.flush()
        self.mutex.release()

    def save_epub(self):
        bookdirpath = os.path.join(self.path, self.bookname)
        bookpath = os.path.join(self.path, '%s.epub' % self.bookname)
        zippath = os.path.join(self.path, '%s.zip' % self.bookname)
        folder = os.path.exists(bookpath)
        if folder:
            os.remove(bookpath)
        shutil.make_archive(bookdirpath, 'zip', bookdirpath)
        os.rename(zippath, bookpath)
        with zipfile.ZipFile(bookpath, 'a') as file:
            file.write(os.path.join(self.template, 'mimetype'), 'mimetype')
        shutil.rmtree(bookdirpath)  # 递归删除文件夹
        print('\r%s.epub 完成' % self.bookname)
