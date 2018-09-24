# -*- coding: utf-8 -*-

import sys
import os
import re
# import pyttsx3 as pyttsx
from lib.novel import Novel

reload(sys)
sys.setdefaultencoding("utf-8")

# engine = pyttsx.init()
# engine.setProperty('volume', 1.0)  # 音量
# engine.setProperty('rate', 200)  # 语速

if __name__ == "__main__":
    novels = []
    website = 0  # xiashu = 0, biquge = 1, aishu = 2, mianhuatang = 3
    down_mode = Novel.Normal
    mode = Novel.Search_Name
    driver_name = Novel.Chrome
    if len(sys.argv) > 1:
        for i in xrange(1, len(sys.argv)):
            arg = str(sys.argv[i])
            if arg.startswith('-'):
                _arg = arg.lower()
                for se in _arg.replace('-', ''):
                    if se == 'r':
                        down_mode = Novel.ReDownload
                    elif se == 'n':
                        down_mode = Novel.Normal
                    elif se == 'c':
                        driver_name = Novel.Chrome
                    elif se == 'f':
                        driver_name = Novel.FireFox
                    elif re.match(r'[0-3]', se):
                        website = int(se)
                    else:
                        print '\t', u'-n 更新或创建（默认）'
                        print '\t', u'-r 替换或创建'
                        print '\t', u'-c 使用Chrome浏览器（默认）'
                        print '\t', u'-f 使用FireFox浏览器'
                        print '\t', u'-[0-3] 下书网=0（默认）, 笔趣阁=1, 爱书网=2, 棉花糖=3'
                        sys.exit(0)
            else:
                novels.append(arg)
    else:
        novels = [u'修炼狂潮']

    if not novels:
        name = raw_input(unicode('书名（多个以空格隔开）：', 'utf-8').encode('gbk'))
        novels = name.split(' ')
    for novel in novels:
        if not isinstance(novel, unicode):
            novel = unicode(novel, 'gbk')
        # engine.say(u'开始抓取 %s' % novel)
        # engine.runAndWait()
        Novel(novel, mode, down_mode, website)
    if len(novels) > 0:
        path = os.path.abspath('file/novel')
        os.system('explorer /e,"%s"' % path)
    # engine.say(u'抓取完成')
    # engine.runAndWait()
