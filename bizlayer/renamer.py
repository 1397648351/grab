# -*- coding: utf-8 -*-

import sys, os, threading

reload(sys)
sys.setdefaultencoding("utf-8")


class Renamer:
    def __init__(self):
        self.path = "E:/Project/PHP/wu/public/static/dist/images/xiezhen/xinggan/"

    def rename(self, name):
        path = os.path.join(self.path, name)
        if os.path.isdir(path):
            if os.path.exists(os.path.join(path, '000.jpg')):
                if os.path.exists(os.path.join(path, '001.jpg')):
                    os.remove(os.path.join(path, '000.jpg'))
                else:
                    os.rename(os.path.join(path, '000.jpg'), os.path.join(path, '001.jpg'))

    def start(self):
        threads = []
        dirs = os.listdir(self.path)
        for name in dirs:
            th = threading.Thread(target=self.rename, args=(name,))
            th.start()
            threads.append(th)
        for th in threads:
            th.join()
