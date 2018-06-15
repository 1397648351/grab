# -*- coding: utf-8 -*-

import sys, os, urllib2, threading, time, re

reload(sys)
sys.setdefaultencoding('utf-8')


class Grab:
    headers = {
        'Accept-Ranges': "bytes",
        'Content-Type': 'text/html',
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
        'Cache-Control': 'max-age=0',
        # 'Pragma': 'no-cache'
    }
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
                return cls.get_content(url)
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
            if not folder or (folder and not os.path.isdir(path)):
                os.makedirs(path)
            filename = "%s/%s%s" % (path, name, (file_ext) if file_ext else '')
            if os.path.isfile(filename) and os.path.exists(filename):
                print "%s 已存在" % filename
                return False
            content = cls.get_content(url)
            if content:
                with open(filename, 'wb') as f:
                    f.write(content)
            return True
        except Exception, e:
            print '%s %s/%s error:%s' % (url, path, name, str(e))
            return False
        finally:
            cls.mutex.release()


class GrabError(Exception):
    def __init__(self, info):
        Exception.__init__(self, info)
        self.errorinfo = info

    def __str__(self):
        return self.errorinfo
