# -*-coding:utf-8-*-

import sys

from lib.novel_epub import Novel
import pyttsx

reload(sys)
sys.setdefaultencoding("utf-8")

if __name__ == "__main__":
    novels = [u'绝世武神']
    engine = pyttsx.init()
    # voices = engine.getProperty('voices')
    # for voice in voices:
    #     print voice
    # engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_KANGKANG_11.0')  # 发音人
    engine.setProperty('volume', 1.0)  # 音量
    engine.setProperty('rate', 200)  # 语速
    for novel in novels:
        engine.say(u'开始抓取 %s' % novel)
    engine.runAndWait()
    # ss = Novel(novel, 1, 0)
    engine.say(u'抓取完成')
    engine.runAndWait()
