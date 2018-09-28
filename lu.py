# -*- coding: utf-8 -*-

import sys
from bizlayer.lu import Lu

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == "__main__":
    lu = Lu(2, 30, 30)
    lu.getpages()
