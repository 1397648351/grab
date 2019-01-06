# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time   : 2018/12/27 23:13
# @Author : WuZe
# @Desc   :
# ==================================================

import sys
import os
import re
import threading
from lib.grab import Grab
from lib.db import DB
from pyquery import PyQuery as pq

reload(sys)
sys.setdefaultencoding('UTF-8')


class Movies:
    def __init__(self):
        self.domain = 'https://www.dytt8.net'
        # self.url = '/html/gndy/dyzz/index.html'
        self.imgpath = 'E:/Project/PHP/bit/public/static/dist/images/movies'
        self.async = 6
        self.idList = []
        self.movies = []
        # self.sqlList = []
        self.imgList = []

    def makedir(self):
        path = os.path.abspath(self.imgpath)
        if not os.path.exists(os.path.abspath(path)):
            os.makedirs(path)

    def run(self, limit, to=0):
        ids = DB.fetchall("SELECT id from bs_movie")
        for id in ids:
            self.idList.append(str(id[0]))
        print '正在抓取....'
        # self.makedir()
        if to == 0:
            nums = xrange(limit)
        else:
            nums = xrange(limit, to + 1)
        threads = []
        for i in nums:
            url = self.domain + '/html/gndy/dyzz/list_23_%s.html' % (i + 1)
            th = threading.Thread(target=self.get_page, args=(url,))
            th.start()
            threads.append(th)
            while len(threads) >= self.async / 2:
                for j, _th in enumerate(threads):
                    if not _th.isAlive():
                        threads.pop(j).join()
        while len(threads) > 0:
            for i, _th in enumerate(threads):
                if not _th.isAlive():
                    threads.pop(i).join()
        threads = []
        num = len(self.movies)
        print '共%s' % num
        for link in self.movies:
            th = threading.Thread(target=self.get_movie, args=(link,))
            th.start()
            threads.append(th)
            while len(threads) >= self.async / 2:
                for j, _th in enumerate(threads):
                    if not _th.isAlive():
                        threads.pop(j).join()
                        num = num - 1
                        print '剩%s' % num
        while len(threads) > 0:
            for i, _th in enumerate(threads):
                if not _th.isAlive():
                    threads.pop(i).join()
                    num = num - 1
                    print '剩%s' % num
        # print '正在入库....'
        # if len(self.sqlList) > 0:
        #     DB.doTrans(self.sqlList)
        DB.execute(
            "DELETE from bs_movie where id in (select a.id from (SELECT min(id) as id FROM bs_movie GROUP BY name HAVING count(name) > 1) a)")

    def get_page(self, url):
        html = Grab.get_content(url).replace('xmlns="http://www.w3.org/1999/xhtml" /', '').replace(
            'xmlns="http://www.w3.org/1999/xhtml"', '').decode('gb2312', 'ignore')
        doc = pq(html)
        items = doc('.co_content8 table tr:eq(1) td:eq(1) a').items()
        for item in items:
            link = self.domain + item.attr('href')
            self.movies.append(link)

    def get_movie(self, url):
        try:
            sqlList = []
            info = {
                'id': '',
                'name': '',
                'date': None,
                'score': '0',
                'introduction': '',
                'download': '',
            }
            pattern = re.compile(r'.*/(?P<id>\d*)\.html')
            info['id'] = re.search(pattern, url).group('id')
            if info['id'] in self.idList:
                return
            html = Grab.get_content(url).replace('xmlns="http://www.w3.org/1999/xhtml" /', '').replace(
                'xmlns="http://www.w3.org/1999/xhtml"', '').decode('gb2312', 'ignore')
            doc = pq(html)
            info['download'] = doc('#Zoom table td:first-child').eq(0).text()
            name = doc('.bd3r .co_area2 .title_all h1').text()
            info['name'] = re.search(ur'.*《(.*)》.*', name).group(1)
            # name = re.search(ur'.*阳光电影www\.ygdy8\.com\.(\W*\d?)\..*', info['download']).group(1).strip()
            content = doc('#Zoom p:first-child')
            if not content:
                return
            content = content.remove('br').html().replace('　', '')
            pattern = re.compile(ur'.*◎年代.*(?:.*/)?(?P<date>\d{4}[-年]\d{2}[-月]\d{2}日?)\(.*')
            res = re.match(pattern, content)
            if res:
                info['date'] = res.group('date').strip().replace('年', '-').replace('月', '-').replace('日', '-')
            pattern = re.compile(ur'.*◎豆瓣评分(?P<score>.*)/10 from .* users.*')
            res = re.match(pattern, content)
            if res:
                info['score'] = res.group('score').strip()
                if not info['score']:
                    info['score'] = '0'
            else:
                pattern = re.compile(ur'.*◎IMDb评分(?P<score>.*)/10 from .* users.*', re.I)
                res = re.match(pattern, content)
                if res:
                    info['score'] = res.group('score').strip()
                    if not info['score']:
                        info['score'] = '0'
            pattern = re.compile(ur'.*◎简介(?P<introduction>.*)◎获奖情况.*<img.*')
            res = re.match(pattern, content)
            if res:
                info['introduction'] = res.group('introduction').strip().replace('\'', '\\\'')
            else:
                pattern = re.compile(ur'.*◎简介(?P<introduction>.*).*<img.*')
                res = re.match(pattern, content)
                if res:
                    info['introduction'] = res.group('introduction').strip().replace('\'', '\\\'')
            if len(info['introduction']) >= 1024:
                info['introduction'] = ''
            # print info['introduction'], url
            # return
            sql = "select * from bs_movie where name='%s' or id='%s'" % (info['name'], info['id'])
            res = DB.fetchone(sql)
            if res:
                if int(info['id']) > res[0]:
                    sql = "delete from bs_movie where id='%s'" % res[0]
                    sqlList.append(sql)
                    # self.sqlList.append(sql)
                else:
                    return
            if info['date']:
                sql = "insert into bs_movie (id,name,date,score,introduction,url,download) values ('%s','%s','%s','%s','%s','%s','%s')" % (
                    info['id'], info['name'], info['date'], info['score'], info['introduction'], url,
                    info['download'])
            else:
                sql = "insert into bs_movie (id,name,date,score,introduction,url,download) values ('%s','%s',NULL,'%s','%s','%s','%s')" % (
                    info['id'], info['name'], info['score'], info['introduction'], url,
                    info['download'])
            # print sql
            sqlList.append(sql)
            if len(sqlList) == 1:
                DB.execute(sqlList[0])
            else:
                DB.doTrans(sqlList)
            # self.sqlList.append(sql)
        except Exception, ex:
            print str(ex), url


if __name__ == "__main__":
    m = Movies()
    m.run(11, 50)
    # m.get_movie('https://www.dytt8.net/html/gndy/dyzz/20170414/53727.html')
