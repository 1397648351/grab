# -*-coding:utf-8-*-

import sys

from lib.novel import Novel

reload(sys)
sys.setdefaultencoding("utf-8")


if __name__ == "__main__":
    novel = Novel()
    novel.get_chapter()
