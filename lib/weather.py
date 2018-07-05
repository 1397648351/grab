#!/usr/local/bin/python
# -*-coding:utf-8-*-

import sys
import requests
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
    print u'城  市：%s' % data.get('city')
    print u'舒适度：%s' % data.get('ganmao')
    print '\r'
    for cur in data.get('forecast'):
        print u'%s：' % cur.get('date')
        print u'\t%s：' % cur.get('date')
        print '\r'
except Exception, ex:
    print ex.message



# req = urllib2.Request('http://wthrcdn.etouch.cn/weather_mini?city=%s' % u'南京')
# req.add_header('User-Agent',
#                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
# res = urllib2.urlopen(req).read()
# res = zlib.decompress(res, zlib.MAX_WBITS | 16).decode('utf-8')
# res = json.loads(res)
