# -*-coding:utf-8-*-

import sys, re
from lib.grab import Grab

reload(sys)
sys.setdefaultencoding("utf-8")

if __name__ == "__main__":
    # Grab.get_content('https://www.fffff.com/')
    Grab.download_image('https://csdnimg.cn/release/phoenix/themes/big-white/images/bg-title.png?v4', 'file', '1.png')
