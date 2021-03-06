# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time   : 2018/12/27 23:13
# @Author : WuZe
# @Desc   :
# ==================================================

import sys, os, re
import signal
# import pyttsx3 as pyttsx
from bizlayer.novel import Novel


# engine = pyttsx.init()
# engine.setProperty('volume', 1.0)  # 音量
# engine.setProperty('rate', 200)  # 语速

def signal_handler(signalnum, frame):
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    novels = []
    website = 2   # biquge = 0, aishu = 1, mianhuatang = 2, blvo = 3
    down_mode = Novel.Normal
    mode = Novel.Search_Name
    driver_name = Novel.Chrome
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
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
                        print('\t', '-n 更新或创建（默认）')
                        print('\t', '-r 替换或创建')
                        print('\t', '-c 使用Chrome浏览器（默认）')
                        print('\t', '-f 使用FireFox浏览器')
                        print('\t', '-[0-3] 笔趣阁=0（默认）, 爱书网=1, 棉花糖=2, 80电子书=3')
                        sys.exit(0)
            else:
                novels.append(arg)

    # 自用
    else:
        novels = ['星战风暴']

    if not novels:
        name = input('书名（多个以空格隔开）：')
        novels = name.split(' ')
    for novel in novels:
        # if not isinstance(novel, unicode):
        #     novel = novel.decode('gbk')
        # engine.say('开始抓取 %s' % novel)
        # engine.runAndWait()
        Novel(novel, mode, down_mode, website)
    if len(novels) > 0:
        path = os.path.abspath(os.path.join(sys.path[0], 'file/novel')) #, '%s.epub' % novels[0]
        os.system('explorer /e,"%s"' % path)
    # engine.say('抓取完成')
    # engine.runAndWait()
