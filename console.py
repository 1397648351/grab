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
    print len('av')
    res = [
        [ur'(?<=[。，”！？]).{1,16}最新章节', ur''],
        [ur'<p>.{1,16}最新章节</p>', ur'']
    ]
    with open('file/temp.xhtml', 'r') as f:
        _str = f.read().decode('utf-8', 'ignore')
        for item in res:
            _str = re.sub(item[0], item[1], _str, flags=re.M)
        with open('file/temp1.xhtml', 'w') as f1:
            f1.write(_str)
    # _str = u'不过对于楚云凡来说，还是很兴奋的，从小他也没能接触到武技，虽然他知道，现在这年头要学武技很简单，一些低级的武技，在网上都年头学的到，只要付出一些金钱就可以了。英雄联盟之灾变时代最新章节'
    # strs, n = re.subn(ur'.*(年头).*', ur'\1\2', _str)
    # print n
    # print strs

    # engine = pyttsx.init()
    # engine.setProperty('volume',1.0)
    # engine.setProperty('rate',200)
    # engine.say('第九百二十二章')
    # engine.runAndWait()leep(1)
