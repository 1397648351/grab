# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time   : 2018/12/27 23:13
# @Author : WuZe
# @Desc   :
# ==================================================

import sys
import requests
import re
import time
import json
import zlib
import urllib2

reload(sys)
sys.setdefaultencoding('utf-8')

'''
( de ) 反向代理 deflate格式，请使用 wbits = -zlib.MAX_WBITS
( de ) 反向代理 zlib格式，请使用 wbits = zlib.MAX_WBITS
( de ) 反向代理 gzip格式，请使用 wbits = zlib.MAX_WBITS | 16
'''

try:
    print(u'------天气查询------')
    data = {'city': u'南京'}
    res = requests.get('http://wthrcdn.etouch.cn/weather_mini', params=data).json()
    data = res.get('data')
    forecast = data.get('forecast')
    r_fl = re.compile(r'<!\[CDATA\[(.*)\]\]>')
    r_wd = re.compile(r'.* (.*)')
    r_date = re.compile(ur'(.{1,2}日).*')
    print u'城  市：%s' % data.get('city')
    print u'天  气：%s' % forecast[0].get('type')
    print u'温  度：%s' % data.get('wendu')
    print u'风  向：%s' % forecast[0].get('fengxiang')
    print u'风  力：%s' % r_fl.match(forecast[0].get('fengli')).group(1)
    print u'最  高：%s' % r_wd.match(forecast[0].get('high')).group(1)
    print u'最  低：%s' % r_wd.match(forecast[0].get('low')).group(1)
    print u'空  气：%s' % data.get('aqi')
    print u'舒适度：%s' % data.get('ganmao')
    for i in xrange(0, 5):
        cur = forecast[i]
        print '\r'
        str_date = time.strftime(u'%Y年%m月') + r_date.match(cur.get('date')).group(1)
        date = time.strptime(str_date, u'%Y年%m月%d日')
        # print int(time.mktime(date))
        # print time.strftime('%Y年%m月%d日', date)
        print u'%s：' % time.strftime('%Y年%m月%d日', date)
        print u'\t天气：%s' % cur.get('type')
        print u'\t风向：%s' % cur.get('fengxiang')
        print u'\t风力：%s' % r_fl.match(cur.get('fengli')).group(1)
        print u'\t最高：%s' % r_wd.match(cur.get('high')).group(1)
        print u'\t最低：%s' % r_wd.match(cur.get('low')).group(1)
except Exception, ex:
    print ex.message

# req = urllib2.Request('http://wthrcdn.etouch.cn/weather_mini?city=%s' % u'南京')
# req.add_header('User-Agent',
#                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
# res = urllib2.urlopen(req).read()
# res = zlib.decompress(res, zlib.MAX_WBITS | 16).decode('utf-8')
# res = json.loads(res)
