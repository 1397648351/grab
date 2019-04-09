# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time   : 2019/4/8 18:21
# @Author : WuZe
# @Desc   :
# ==================================================

import os, urllib.request, threading, time, re, random


class Spider:
    headers = [{
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }, {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'
    }]
    proxy_info = {
        'host': '115.223.205.157',
        'port': 9000
    }
    use_proxy = False
    timeout = 30
    mutex = threading.RLock()  # 创建锁

    def __init__(self, url):
        """
        Grab init
        :param url: URL
        """
        self.url = url

    @classmethod
    def get_content(cls, url, headers_add=None, cookies=None):
        """
        获取网页内容
        :param url:
        :return: 网页内容
        """
        if not url:
            raise Exception(u"URL不能为空")
        if cls.use_proxy:
            # We create a handler for the proxy
            proxy_support = urllib.request.ProxyHandler({"http": "http://%(host)s:%(port)d" % cls.proxy_info})
            # We create an opener which uses this handler:
            opener = urllib.request.build_opener(proxy_support)
            # Then we install this opener as the default opener for urllib.request:
            urllib.request.install_opener(opener)
        index = random.randint(0, len(cls.headers) - 1)
        headers = cls.headers[index]
        request = urllib.request.Request(url, headers=headers)
        if headers_add:
            for key in headers_add:
                request.add_header(key, headers_add[key])
                # headers['Referer'] = headers_referer
        if cookies:
            str_cookie = ''
            for key in cookies:
                str_cookie = '%s%s=%s;' % (str_cookie, key, cookies[key])
            if str_cookie:
                request.add_header('Cookie', str_cookie)
        try:
            response = urllib.request.urlopen(request, timeout=cls.timeout)
            return response.read()
        except urllib.request.URLError as e:
            restart = True
            codes = ['304', '400', '401', '403', '404', '11001']
            if hasattr(e, 'code'):
                code = e.code
            elif hasattr(e, 'reason'):
                pattern = re.compile(r'\[.* (\d+)\]', re.M)
                m = pattern.match(str(e.reason))
                if m:
                    code = m.group(1)
            if 'code' in vars() and str(code) in codes:
                cls.mutex.acquire()
                restart = False
                print('Error Code: %s, URL: %s' % (code, url))
                cls.mutex.release()
            else:
                cls.mutex.acquire()
                print(url, e.reason)
                cls.mutex.release()
            if restart:
                time.sleep(1)
                return cls.get_content(url)
            else:
                return None

    @classmethod
    def download_image(cls, url, path, name, noprint=False, headers_referer=None):
        """
        下载图片
        :param url: URL
        :param path: 保存路径
        :param name: 文件名
        """
        if not url:
            raise Exception(u"URL不能为空")
        try:
            pattern = re.compile(r'.*(\.bmp|\.jpg|\.jpeg|\.png|\.gif).*', re.I)
            m = pattern.match(url)
            file_ext = '.jpg'
            if m:
                file_ext = m.group(1)
            cls.mutex.acquire()
            folder = os.path.exists(path)
            if not folder or (folder and not os.path.isdir(path)):
                os.makedirs(path)
            filename = "%s/%s%s" % (path, name, (file_ext) if file_ext else '')
            confirm = os.path.isfile(filename) and os.path.exists(filename)
            cls.mutex.release()
            if confirm:
                if not noprint:
                    print("%s 已存在" % filename)
                return False
            headers_add = None
            if headers_referer:
                headers_add = {'Referer': headers_referer}
            content = cls.get_content(url, headers_add=headers_add)
            if content:
                with open(filename, 'wb') as f:
                    f.write(content)
            if not noprint:
                print('%s 下载完成！' % filename)
            return True
        except Exception as e:
            print('%s %s/%s error:%s' % (url, path, name, str(e)))
            return False
