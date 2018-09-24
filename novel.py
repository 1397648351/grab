# -*- coding: utf-8 -*-

import sys
# import pyttsx3 as pyttsx
from lib.novel import Novel

reload(sys)
sys.setdefaultencoding("utf-8")

# engine = pyttsx.init()
# engine.setProperty('volume', 1.0)  # 音量
# engine.setProperty('rate', 200)  # 语速

if __name__ == "__main__":
    novels = []
    if len(sys.argv) > 1:
        for i in xrange(1, len(sys.argv)):
            novels.append(sys.argv[i])
    else:
        novels = [u'修炼狂潮']
    mode = Novel.Search_Name
    down_mode = Novel.Normal
    website = 0  # xiashu = 0, biquge = 1, aishu = 2, mianhuatang = 3

    if not novels:
        name = raw_input(u'书名：')
        novels.append(name)
        mode = raw_input(u'根据ID搜索输入0，根据书名搜索输入1：')
        down_mode = raw_input(u'下载或更新输入0，重新下载输入1：')
    for novel in novels:
        if not isinstance(novel, unicode):
            novel = unicode(novel, 'gbk')
        # engine.say(u'开始抓取 %s' % novel)
        # engine.runAndWait()
        Novel(novel, mode, down_mode, website)
    # engine.say(u'抓取完成')
    # engine.runAndWait()
