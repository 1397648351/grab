# -*-coding:utf-8-*-

import sys

from lib.novel_epub import Novel
import pyttsx

reload(sys)
sys.setdefaultencoding("utf-8")

if __name__ == "__main__":
    novels = [u'老衲要还俗']
    engine = pyttsx.init()
    engine.say('开始')
    engine.runAndWait()
    for novel in novels:
        ss = Novel(novel, Novel.SEARCH_NAME, Novel.REDOWNLOAD)
    engine.say('结束')
    engine.runAndWait()
