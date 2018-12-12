# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from lib.grab import Grab
from pyquery import PyQuery as pq

reload(sys)
sys.setdefaultencoding('UTF-8')


class Movies:
    def __init__(self):
        self.domain = 'https://www.dytt8.net'
        self.url = '/html/gndy/dyzz/index.html'

    def run(self):
        url = self.domain + self.url
        html = Grab.get_content(url).replace('xmlns="http://www.w3.org/1999/xhtml" /', '').replace(
            'xmlns="http://www.w3.org/1999/xhtml"', '').decode('gb2312', 'ignore')
        doc = pq(html)
        items = doc('.co_content8 table tr:eq(1) td:eq(1) a').items()
        for item in items:
            title = item.text()
            pattern = re.compile(ur'.*《(.*)》.*')
            matchObj = re.match(pattern, title)
            if matchObj:
                print matchObj.group(1)


if __name__ == "__main__":
    m = Movies()
    m.run()
