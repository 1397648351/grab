# -*- coding: utf-8 -*-

import sys
import pyttsx

reload(sys)
sys.setdefaultencoding("utf-8")

engine = pyttsx.init()
engine.setProperty('volume', 1.0)  # 音量
engine.setProperty('rate', 200)  # 语速

if __name__ == "__main__":
    engine.say(u'开始抓取 %s' % 'avc')
    engine.runAndWait()
    engine.say(u'抓取完成')
    engine.runAndWait()
