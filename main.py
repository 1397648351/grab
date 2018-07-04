# -*-coding:utf-8-*-

import sys

from lib.novel_epub import Novel
import pyttsx

reload(sys)
sys.setdefaultencoding("utf-8")

if __name__ == "__main__":
    novels = [u'绝世武神']
    engine = pyttsx.init()
    for novel in novels:
        engine.say(u'开始抓取 %s' % novel)
        engine.runAndWait()
        ss = Novel(novel, 1, 0)
    engine.say(u'抓取完成')
    engine.runAndWait()
