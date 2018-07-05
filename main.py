# -*-coding:utf-8-*-

import sys

from lib.novel_epub import Novel
import pyttsx

reload(sys)
sys.setdefaultencoding("utf-8")

if __name__ == "__main__":
    novels = [u'绝世武神']
    mode = Novel.Search_Name
    down_mode = Novel.Normal
    engine = pyttsx.init()
    if not novels:
        s = raw_input(u'输入：')
        novels.append(s)
        mode = raw_input(u'根据ID搜索输入0，根据书名搜索输入1：')
        down_mode = raw_input(u'下载或更新输入0，重新下载输入1：')
    # engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_KANGKANG_11.0')  # 发音人
    engine.setProperty('volume', 1.0)  # 音量
    engine.setProperty('rate', 200)  # 语速
    for novel in novels:
        engine.say(u'开始抓取 %s' % novel)
        engine.runAndWait()
        # ss = Novel(novel, mode, down_mode)
    engine.say(u'抓取完成')
    engine.runAndWait()
