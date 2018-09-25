# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, time, re
import json
import pyttsx

reload(sys)
sys.setdefaultencoding('UTF-8')

if __name__ == "__main__":
    print os.path.join("E:/", os.path.abspath('D:/a/b'))
    exit(0)
    res = []
    with open('novel.json', 'r') as f:
        conf = json.loads(f.read().decode('utf-8'))
        if conf.has_key('str_replace'):
            res = conf["str_replace"]
    # res = [
    #     [ur'(?<=[。，”！？]).{1,16}最新章节', ur''],
    #     [ur'<p>.{1,16}最新章节</p>', ur'']
    # ]
    with open('file/temp.xhtml', 'r') as f:
        _str = f.read().decode('utf-8', 'ignore')
        for item in res:
            _str = re.sub(item[0], item[1], _str, flags=re.M)
        with open('file/temp1.xhtml', 'w') as f1:
            f1.write(_str)
