# -*- coding: utf-8 -*-

import sys, os, urllib2, threading, time, re

reload(sys)
sys.setdefaultencoding('utf-8')


class Grab:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Cache-Control': 'max-age=0',
        'Pragma': 'no-cache'}
    timeout = 30
    mutex = threading.RLock()  # 创建锁

    def __init__(self, url):
        """
        Grab init
        :param url: URL
        """
        self.url = url

    @classmethod
    def get_content(cls, url):
        """
        获取网页内容
        :param url:
        :return: 网页内容
        """
        if not url:
            raise GrabError(u"URL不能为空")
        request = urllib2.Request(url, headers=cls.headers)
        try:
            response = urllib2.urlopen(request, timeout=cls.timeout)
            return response.read()
        except urllib2.URLError, e:
            restart = True
            codes = '304,400,401,403,404,11001'
            if hasattr(e, 'code'):
                code = e.code
            elif hasattr(e, 'reason'):
                print str(e.reason)
                pattern = re.compile(r'\[.* (\d+)\]', re.M)
                m = pattern.match(str(e.reason))
                if m:
                    code = m.group(1)
            if 'code' in vars() and str(code) in codes:
                restart = False
                print 'Error Code: %s, URL: %s' % (code, url)
            else:
                print e.reason
            if restart:
                time.sleep(1)
                cls.get_content(url)
            else:
                return None

    @classmethod
    def download_image(cls, url, path, name):
        """
        下载图片
        :param url: URL
        :param path: 保存路径
        :param name: 文件名
        """
        if not url:
            raise GrabError(u"URL不能为空")
        cls.mutex.acquire()
        try:
            pattern = re.compile(r'.*(\.bmp|\.jpg|\.jpeg|\.png|\.gif).*', re.I)
            m = pattern.match(url)
            if m:
                file_ext = m.group(1)
            folder = os.path.exists(path)
            if not folder or (folder and os.path.isdir(path)):
                os.makedirs(path)
            filename = "%s/%s%s" % (path, name, (file_ext) if file_ext else '')
            print filename
            if os.path.isfile(filename) and os.path.exists(filename):
                print u"%s 已存在" % filename
                return
            content = cls.get_content(url)
            if content:
                with open(filename, 'wb') as f:
                    f.write(content)
        except Exception, e:
            print e.message
        finally:
            cls.mutex.release()


class GrabError(Exception):
    def __init__(self, info):
        Exception.__init__(self, info)
        self.errorinfo = info

    def __str__(self):
        return self.errorinfo
