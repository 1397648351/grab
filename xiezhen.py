# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from bizlayer.xiezhen import Xiezhen

reload(sys)
sys.setdefaultencoding('UTF-8')

if __name__ == '__main__':
    Xiezhen.start(5)
