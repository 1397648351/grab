# !/usr/bin/env python
# -*-coding: utf-8 -*-

import sys
import os
import time

reload(sys)
sys.setdefaultencoding('UTF-8')


class test:
    def __init__(self):
        self.strlen = 0

    def writeline(self, str):
        s = ''
        if self.strlen > 0:
            for i in xrange(self.strlen):
                s += ' '
            print '\r%s' % s,
            sys.stdout.flush()
            exit(0)
        print '\r%s' % str,
        self.strlen = len(str)
        sys.stdout.flush()


    def ttt(self):
        strs = [
            u'修炼狂潮 [42.49%] 第九百二十二章 一夜之间，仿佛天塌地陷【六更，求订阅】 已存在！',
            u'修炼狂潮 [42.91%] 第九百三十章 群凶出牢笼，形势危如累卵 已存在！',
            u'修炼狂潮 [47.31%] 大家六一节快乐！求月票！ 已存在！'
        ]
        for str in strs:
            self.writeline(str)
            time.sleep(1)


if __name__ == "__main__":
    t = test()
    t.ttt()
