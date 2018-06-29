# -*-coding:utf-8-*-

import sys

from lib.novel_epub import Novel
import pyttsx

reload(sys)
sys.setdefaultencoding("utf-8")

if __name__ == "__main__":
    engine = pyttsx.init()
    engine.say('开始')
    engine.runAndWait()
    ss = Novel()
    ss.get_chapters()
    engine.say('结束')
    engine.runAndWait()
