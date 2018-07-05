# -*- coding: utf-8 -*-

import sys

from lib.novel_epub import Novel
import pyttsx

reload(sys)
sys.setdefaultencoding("utf-8")

engine = pyttsx.init()
engine.setProperty('volume', 1.0)  # 音量
engine.setProperty('rate', 200)  # 语速

if __name__ == "__main__":
    novels = [u'绝世武神']
    mode = Novel.Search_Name
    down_mode = Novel.Normal

    if not novels:
        name = raw_input(u'输入：')
        novels.append(name)
        mode = raw_input(u'根据ID搜索输入0，根据书名搜索输入1：')
        down_mode = raw_input(u'下载或更新输入0，重新下载输入1：')
    for novel in novels:
        engine.say(u'开始抓取 %s' % novel)
        engine.runAndWait()
        Novel(novel, mode, down_mode)
    engine.say(u'抓取完成')
    engine.runAndWait()
