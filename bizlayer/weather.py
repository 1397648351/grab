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
import urllib.request


'''
( de ) 反向代理 deflate格式，请使用 wbits = -zlib.MAX_WBITS
( de ) 反向代理 zlib格式，请使用 wbits = zlib.MAX_WBITS
( de ) 反向代理 gzip格式，请使用 wbits = zlib.MAX_WBITS | 16
'''

try:
    print('------天气查询------')
    data = {'city': '南京'}
    res = requests.get('http://wthrcdn.etouch.cn/weather_mini', params=data).json()
    data = res.get('data')
    forecast = data.get('forecast')
    r_fl = re.compile(r'<!\[CDATA\[(.*)\]\]>')
    r_wd = re.compile(r'.* (.*)')
    r_date = re.compile(r'(.{1,2}日).*')
    print('城  市：%s' % data.get('city'))
    print('天  气：%s' % forecast[0].get('type'))
    print('温  度：%s' % data.get('wendu'))
    print('风  向：%s' % forecast[0].get('fengxiang'))
    print('风  力：%s' % r_fl.match(forecast[0].get('fengli')).group(1))
    print('最  高：%s' % r_wd.match(forecast[0].get('high')).group(1))
    print('最  低：%s' % r_wd.match(forecast[0].get('low')).group(1))
    print('空  气：%s' % data.get('aqi'))
    print('舒适度：%s' % data.get('ganmao'))
    for i in range(0, 5):
        cur = forecast[i]
        print('\r')
        str_date = time.strftime('%Y年%m月') + r_date.match(cur.get('date')).group(1)
        date = time.strptime(str_date, '%Y年%m月%d日')
        # print(int(time.mktime(date)))
        # print(time.strftime('%Y年%m月%d日', date))
        print('%s：' % time.strftime('%Y年%m月%d日', date))
        print('\t天气：%s' % cur.get('type'))
        print('\t风向：%s' % cur.get('fengxiang'))
        print('\t风力：%s' % r_fl.match(cur.get('fengli')).group(1))
        print('\t最高：%s' % r_wd.match(cur.get('high')).group(1))
        print('\t最低：%s' % r_wd.match(cur.get('low')).group(1))
except Exception as ex:
    print(str(ex))

# req = urllib.request.Request('http://wthrcdn.etouch.cn/weather_mini?city=%s' % '南京')
# req.add_header('User-Agent',
#                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
# res = urllib.request.urlopen(req).read()
# res = zlib.decompress(res, zlib.MAX_WBITS | 16).decode('utf-8')
# res = json.loads(res)
