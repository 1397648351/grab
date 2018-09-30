# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, signal
from bizlayer.xiezhen import Xiezhen

reload(sys)
sys.setdefaultencoding('UTF-8')

kinds = ['xinggan', 'qingchun', 'xiaohua', 'chemo', 'qipao', 'mingxing']


def sigint_handler(signum, frame):
    global xz, is_stopped
    xz.stop()
    is_stopped = True
    while xz.run:
        pass
    sys.exit(0)


if __name__ == '__main__':
    xz = Xiezhen(1, kind=kinds[0])
    xz.start()
    is_stopped = False
    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGTERM, sigint_handler)
    while not is_stopped and xz.run:
        pass
