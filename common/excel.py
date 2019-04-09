# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time   : 2019/4/9 14:46
# @Author : WuZe
# @Desc   : 
# ==================================================

import xlrd
import xlwt
import threading
from xlutils.copy import copy

mutex = threading.RLock()  # 创建锁


def new_excel(sheetname, filepath):
    print('发现写入目标不存在，正在创建文件', filepath)
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    book.add_sheet(sheetname, cell_overwrite_ok=True)
    book.save(filepath)
    print('已成功创建文件', filepath)


def repeat_excel(word, sheetname, filepath):
    # print u'正在检测', word, u'是否存在于文件中'
    try:
        workbook = xlrd.open_workbook(filepath)
        sheet = workbook.sheet_by_name(sheetname)
        words = sheet.col_values(0)
        if word in words:
            # print u'在excel中已经存在', word, u'跳过'
            return True
        else:
            # print u'在excel中不存在'
            return False
    except IOError as e:
        if 'No such file' in e.strerror:
            print('匹配重复时未找到该文件', filepath)
            new_excel(filepath)
            return False
    return False


def write_to_excel(contents, file):
    if contents:
        print('正在写入到文本中', contents['name'])
        try:
            rb = xlrd.open_workbook(file)
            sheet = rb.sheets()[0]
            row = sheet.nrows
            wb = copy(rb)
            sheet = wb.get_sheet(0)
            id = contents['id']
            if not repeat_excel(id, file):
                sheet.col(1).width = 100 * 256
                sheet.col(2).width = 100 * 256
                sheet.col(3).width = 15 * 256
                sheet.col(4).width = 20 * 256
                sheet.write(row, 0, contents['id'])
                sheet.write(row, 1, contents['name'])
                sheet.write(row, 2, contents['html'])
                sheet.write(row, 3, contents['time'])
                sheet.write(row, 4, contents['types'])
                wb.save(file)
                print
                u'已成功写入到文件', file, u'第', row + 1, u'行'
            else:
                print
                u'内容已存在, 跳过写入文件', file
        except IOError:
            new_excel(file)
            write_to_excel(contents, file)


def write_info(info):
    mutex.acquire()
    write_to_excel(info)
    mutex.release()
