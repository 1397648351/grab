# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re, signal,time
import string
from bizlayer.xiezhen import Xiezhen

reload(sys)
sys.setdefaultencoding('UTF-8')

#is_sigint_up = False



if __name__ == '__main__':
    xz = Xiezhen(1)
    xz.start()
    def sigint_handler(signum, frame):
        is_sigint_up = True
        print 'catched interrupt signal!'
        sys.exit(0)
    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGTERM, sigint_handler)
    is_sigint_up = False

    while not is_sigint_up:
        print 'aaaa'
        time.sleep(2)