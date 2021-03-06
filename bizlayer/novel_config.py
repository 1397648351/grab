# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time   : 2018/12/27 23:13
# @Author : WuZe
# @Desc   :
# ==================================================

import time


def ele_click(driver):
    element = driver.find_element_by_id("yc")
    element.click()
    element = driver.find_element_by_id("zkzj")
    while element.text != '点击关闭':
        time.sleep(0.1)


biquge = 0
aishu = 1
mianhuatang = 2
blvo = 3

SAVE_PATH = 'file/novel'

settings = [
    {
        'home': 'https://www.biquge5200.cc',
        'decode': 'gbk',
        'book': {
            'input': 'wd',
            'submit': 'sss',
            'link': '#hotcontent table.grid tr:gt(0)',
            'href': 'td.odd:nth-child(1) a',
            'link_replace': 'https://www.biquge5200.cc/'
        },
        'page': {
            'rm_eles': [],
            'do': None,
            'name': '#info h1',
            'introduction': '#intro',
            'creator': '#info>p:nth-child(2)',
            'cover': '#fmimg img',
            'chapters': '#list dd:gt(8)',
            'link_concat': False
        },
        'chapter': {
            'rm_eles': [],
            'content': '#content',
            'gzip': False
        },
    },
    {
        'home': 'https://www.22ff.org/',
        'decode': 'gbk',
        'book': {
            'input': 'sk',
            'submit': 'searcher',
            'link': '.neirong ul:gt(0)',
            'href': 'li.neirong1 a:lt(1)',
            'link_replace': ''
        },
        'page': {
            'rm_eles': ['h4'],
            'do': None,
            'name': '.tname a',
            'introduction': 'table.fw tr:nth-child(4)',
            'creator': 'table.fw tr:nth-child(1) td:nth-child(3) a',
            'cover': 'img.novel_cover',
            'chapters': '.neirong .clc',
            'link_concat': True
        },
        'chapter': {
            'rm_eles': ['#chapter_content script'],
            'content': '#chapter_content',
            'gzip': False
        },
    },
    {
        'home': 'http://www.mianhuatang520.com/',
        'decode': 'GB2312',
        'book': {
            'input': 'bookname',
            'submit': 'sss',
            'link': '#newscontent>.l>ul>li',
            'href': '.s2>a',
            'link_replace': 'http://www.mianhuatang520.com/'
        },
        'page': {
            'rm_eles': [],
            'do': None,
            'name': '#info h1',
            'introduction': '#intro',
            'creator': '#info div:nth-child(2)',
            'cover': '#fmimg>img',
            'chapters': '#list>dl>dd',
            'link_concat': False
        },
        'chapter': {
            'rm_eles': ['#zjneirong>div'],
            'content': '#zjneirong',
            'gzip': False
        },
    },
    {
        'home': 'https://www.80vo.com/',
        'decode': 'utf-8',
        'book': {
            'input': 'shuming',
            'submit': 'submitbtn',
            'link': '#waterfall .item.masonry-brick',
            'href': '.title h3 a',
            'link_replace': '/api/ajax/searchid.php?id='
        },
        'page': {
            'rm_eles': ['#aboutbook a.fr', '#aboutbook h3'],
            'do': ele_click,
            'name': '#info .infotitle h1',
            'introduction': '#aboutbook',
            'creator': '.ainfo .username a',
            'cover': '#picbox .img_in img',
            'chapters': '#detaillist ul li',
            'link_concat': True
        },
        'chapter': {
            'rm_eles': ['#chaptercontent #tac'],
            'content': '#chaptercontent',
            'gzip': False
        },
    },
]

str_replace = [
    '一秒记住【棉花糖小说网mianhuatang.la】，为您提供精彩小说阅读。',
    '一秒记住【谷♂粒÷小÷说→网 xinguli】，更新快，无弹窗，免费读！',
    '一秒记住【谷♂粒÷网 xinguli】，精彩小说无弹窗免费阅读！',
    'c_t;', 'reads;', '（ 广告）', '( $&gt;&gt;&gt;棉、花‘糖’小‘說’)',
    '( $>>>棉、花‘糖’小‘說’)', '( )', '（ ）', '[ ]', '（ 棉花糖', '( ’)', '【】',
    '[看本书最新章节请到]', '[更新快，网站页面清爽，广告少，，最喜欢这种网站了，一定要好评]',
    '其c他都5是w盗版0`', '天才壹秒記住愛♂去÷小說→網，為您提供精彩小說閱讀。',
    '~搜搜篮色，即可全文阅读后面章节', '-79-', '-79xs-', '&amp;nnsp;', '天才壹秒記住『笔下文学 qu 】”',
    '天才壹秒記住『笔下文学 qu 】',
    '最新章节全文阅读。更多最新章节访问:ww 。', '。 更新好快。', '天才壹秒記住『笔下文学 』，為您提供精彩小說閱讀。',
    '最新章节全文阅读', '。更多最新章节访问:ww 。', 'ＷｗΔＷ．『ksnhuge『ge．La',
    '[想看的书几乎都有啊，比一般的站要稳定很多更新还快，全文字的没有广告。]',
    '恋上你看书网 630bookla ，最快更新神豪无极限最新章节！', 'readx;',
    '<br/>　　逐浪推荐游戏<br/><br/>　　三国演义<br/><br/>　　傲视天地<br/><br/>　　屠龙            ',
    'm.22ff.co m', 'm.woquge.co m', 'i.woquge.co m', 'WoQuGe.co m', 'woquge.co m', 'WoQuGe',
    'woquge', 'biquge5200', '恋上你看书网 630bookla ，最快更新__BOOKNAME__最新章节！',
    '〖∷更新快∷无弹窗∷纯文字∷〗', '(请搜索八一，更新最快的站!)', '(请搜索八一，或者直接输入看最新章节)',
    '高速首发__BOOKNAME__最新章节，本章节是地址为如果你觉的本章节还不错的话请不要忘记向您qq群和微博里的朋友推荐哦！',
    '【品文移动阅读-m.pinwenba】', '(  全文阅读)', 'rgstt', 'cqhtg', '{][la}',
    '.co', 'tyjiao', 'tangkx', 'js518pinwenba', 'jlgxhqpinwenba', 'jiaoyu123', 'yacht4s',
    'hotensharepinwenba', 'hotenshare', 'pinwenba', 'weibogg', '【品-文-吧】', 'read3();',
    'ｗww.ranwen.orｇ?', '手机用户请浏览阅读，更优质的阅读体验。',
    [r'(?<=[。，”！？]).{1,16}最新章节', r''], [r'<p>.{1,16}最新章节</p>', r'']
]
