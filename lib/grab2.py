# -*- coding: utf-8 -*-

import sys
import zlib
from pyquery import PyQuery as pq
from lib.grab import Grab

reload(sys)
sys.setdefaultencoding('utf-8')

html = Grab.get_content('http://www.qiushu.cc/t/76658/23612976.html')
# html = html.replace('xmlns="http://www.w3.org/1999/xhtml" /', '')
html = zlib.decompress(html, zlib.MAX_WBITS | 16).decode('utf-8')
doc = pq(html)
doc('.con_l').remove()
doc('#stsm').remove()
# mulu = doc('#content').items()
content = doc('#content').html().replace('&#13;', '').replace('&nbsp;', '')
ps = content.split('<br />')
for p in ps:
    if not p:
        continue
    p = p.strip()
    if not p:
        continue
    print p
