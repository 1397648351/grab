# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pyttsx
import re
import os
import time

reload(sys)
sys.setdefaultencoding('UTF-8')

if __name__ == "__main__":
    res = [r'(</p><p>[。，“]).*最新章节(</p>)', r'\1\2']
    with open('file/temp.xhtml', 'r') as f:
        _str = f.read()
        _str, n = re.subn(res[0], res[1], _str)
        print n
        with open('file/temp1.xhtml', 'w') as f1:
            f1.write(_str)
    # _str = '不过对于楚云凡来说，还是很兴奋的，从小他也没能接触到武技，虽然他知道，现在这年头要学武技很简单，一些低级的武技，在网上都可以学的到，只要付出一些金钱就可以了。英雄联盟之灾变时代最新章节'
    # engine = pyttsx.init()
    # engine.setProperty('volume',1.0)
    # engine.setProperty('rate',200)
    # engine.say('第九百二十二章')
    # engine.runAndWait()leep(1)
