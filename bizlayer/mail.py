# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time   : 2018/12/27 23:13
# @Author : WuZe
# @Desc   :
# ==================================================

import sys
import logging
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

reload(sys)
sys.setdefaultencoding('UTF-8')


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


from_addr = "wuzedc@163.com"
password = "541442573s"
to_addr = "1397648351@qq.com"
smtp_server = "smtp.163.com"

msg = MIMEText('hello,send by Python...', _charset='utf-8')
msg["From"] = _format_addr('爱你的吴 <%s>' % from_addr)
msg['To'] = _format_addr('么么哒 <%s>' % to_addr)
msg['Subject'] = Header('吴对你的问侯', 'utf-8').encode()

if __name__ == "__main__":
    try:
        server = smtplib.SMTP_SSL(smtp_server, 465, timeout=15)
        # server.starttls()
        # server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
    except Exception, e:
        print 'Exception: send email failed', e
