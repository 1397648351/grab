# -*-coding:utf-8-*-

import sys

from lib.novel import Novel
from lib.grab2 import Grab2
from lib.pictures import Pictures
from lib.grab import Grab
from lib.xmlanalysis import XmlAnalysis
from lib.novel2 import Novel2

reload(sys)
sys.setdefaultencoding("utf-8")

if __name__ == "__main__":
    ss = Novel2()
    ss.get_chapters()
    # novel = Novel()
    # novel.get_chapter()
    # pic = Pictures()
    # pic.get_page_url()
    # Grab2.open_content('https://www.xiashu.la/146539/')
    # ele = {
    #     'tag': 'container',
    #     'attrib': {'version': '1.0', 'xmlns': 'urn:oasis:names:tc:opendocument:xmlns:container'},
    #     'children': [
    #         {
    #             'tag': 'rootfiles',
    #             'children': [
    #                 {
    #                     'tag': 'rootfile',
    #                     'attrib': {'full-path': 'content.opf', 'media-type': 'application/oebps-package+xml'}
    #                 }
    #             ]
    #         }
    #     ]
    # }
    # XmlAnalysis.create_xml('file/t.xml', ele)
