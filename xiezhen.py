# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re, signal, time
import string
from bizlayer.xiezhen import Xiezhen

reload(sys)
sys.setdefaultencoding('UTF-8')

kinds = ['xinggan', 'qingchun', 'xiaohua', 'chemo', 'qipao', 'mingxing']

if __name__ == '__main__':
    xz = Xiezhen(1, kind=kinds[1])
    xz.start()


    def sigint_handler(signum, frame):
        global is_stopped
        xz.stop()
        is_stopped = True
        while xz.run:
            pass
        sys.exit(0)


    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGTERM, sigint_handler)
    is_stopped = False
    while not is_stopped and xz.run:
        pass
