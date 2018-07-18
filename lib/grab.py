# -*- coding: utf-8 -*-

import sys, os, urllib2, threading, time, re, random

reload(sys)
sys.setdefaultencoding('utf-8')


class Grab:
    user_agent = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0']
    headers = {
        'User-Agent': user_agent[0],
        'Cache-Control': 'max-age=0',
        'Pragma': 'no-cache'
    }
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
    def get_content(cls, url):
        """
        获取网页内容
        :param url:
        :return: 网页内容
        """
        if not url:
            raise GrabError(u"URL不能为空")
        if cls.use_proxy:
            # We create a handler for the proxy
            proxy_support = urllib2.ProxyHandler({"http": "http://%(host)s:%(port)d" % cls.proxy_info})
            # We create an opener which uses this handler:
            opener = urllib2.build_opener(proxy_support)
            # Then we install this opener as the default opener for urllib2:
            urllib2.install_opener(opener)
        index = random.randint(0, len(cls.user_agent) - 1)
        cls.headers['User-Agent'] = cls.user_agent[index]
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
            file_ext = '.jpg'
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
