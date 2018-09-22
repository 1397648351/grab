# !/usr/bin/env python
# -*-coding: utf-8 -*-

import sys
import pyttsx
import os
import time

reload(sys)
sys.setdefaultencoding('UTF-8')


if __name__ == "__main__":
    engine = pyttsx.init()
    engine.setProperty('volume',1.0)
    engine.setProperty('rate',200)
    engine.say('aaaaaaaaaaa')
    engine.runAndWait()
    '''
    strs = [
        u'修炼狂潮 \033[32m[42.49%]\033[0m 第九百二十二章 一夜之间，仿佛天塌地陷【六更，求订阅】 已存在！',
        u'修炼狂潮 \033[32m[42.91%]\033[0m 第九百三十章 群凶出牢笼，形势危如累卵 已存在！',
        u'修炼狂潮 \033[32m[47.31%]\033[0m 大家六一节快乐！求月票！ 已存在！'
    ]
    for str in strs:
        print '\r%s' % str,
        sys.stdout.flush()
        time.sleep(1)
    '''
