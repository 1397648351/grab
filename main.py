# -*-coding:utf-8-*-

import sys

# from lib.collect import *

reload(sys)
sys.setdefaultencoding("utf-8")


# def calc(head, foot):
#     if foot % 2 != 0:
#         raise RuntimeError('脚的数目不对')
#     for ch in xrange(0, head / 2):  # 鸡最多 head/2 只
#         rab = head - ch
#         _foot = rab * 4 + ch * 2
#         if _foot == foot:
#             return ch, rab
#     raise RuntimeError('无解')


def calc(maxnum):
    for i in xrange(maxnum):
        curnum = i * 2
        if curnum % 4 != 0:
            curnum = curnum / 3 * 5
            if curnum % 6 == 0:
                print i, curnum


if __name__ == "__main__":
    # result = calc(25, 96)
    # if result:
    #     print '鸡%s只，兔%s只' % (result[0], result[1])
    calc(100)
    # Grab.get_content('https://www.fffff.com/')
    # Grab.download_image('https://images2015.cnblogs.com/blog/783328/201605/783328-20160505162146794-19417692.png', 'file', '1.png')
