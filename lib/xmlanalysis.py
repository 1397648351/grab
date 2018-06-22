# -*- coding: utf-8 -*-
import sys
from xml.etree import ElementTree as ET

reload(sys)
sys.setdefaultencoding('utf-8')


class XmlAnalysis:
    def __init__(self):
        self.version = '1.0'

    @staticmethod
    def create_xml(path, ele):
        if not path:
            raise Exception(u"文件名不能为空")
        root = XmlAnalysis.add_element(ele)
        tree = ET.ElementTree(root)
        tree.write(path)

    @staticmethod
    def add_element(eles, root=None):
        if not eles:
            raise Exception(u'eles不能为空')
        if not isinstance(eles, list):
            if not root:
                if not eles['attrib']:
                    eles['attrib'] = {}
                element = ET.Element(eles['tag'], eles['attrib'])
                if eles['children']:
                    XmlAnalysis.add_element(eles['children'], element)
                return element
        else:
            if root is None:
                raise Exception(u'root不能为空')
            for ele in eles:
                print ele['tag']
                if not ele['attrib']:
                    ele['attrib'] = {}
                element = ET.SubElement(root, ele['tag'], ele['attrib'])
                if 'children' in ele.keys():
                    XmlAnalysis.add_element(ele['children'], element)
