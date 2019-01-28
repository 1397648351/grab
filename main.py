# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time   : 2018/12/27 23:13
# @Author : WuZe
# @Desc   :
# ==================================================

import os, re


if __name__ == "__main__":
    path = os.path.abspath("E:/Music")
    files = os.listdir(path)
    for name in files:
        # name = name.decode('gbk').encode('utf-8')
        file_path = os.path.join(path, name)
        if not os.path.isdir(file_path):
            pattern = re.compile(r'(.*)(\(\d{1,2}\))', re.U | re.S)
            matchObj = re.match(pattern, name)
            if matchObj:
                # print matchObj.group(1)
                os.remove(file_path)
                print('删除', name.decode('gbk').encode('utf-8'))
