# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time   : 2018/12/27 23:13
# @Author : WuZe
# @Desc   :
# ==================================================

import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

reload(sys)
sys.setdefaultencoding('UTF-8')

try:
    driver = webdriver.Chrome()
    driver.get('https://www.baidu.com')
    WebDriverWait(driver, 30, .5).until(EC.presence_of_all_elements_located((By.ID, "kw")))
    input = driver.find_element(By.ID, 'kw')
    input.send_keys(u"我的天")
    input.send_keys(Keys.ENTER)
    try:
        WebDriverWait(driver, 30, .5).until(EC.presence_of_all_elements_located((By.ID, "1")))
    except:
        print("ele can't find")
        exit(0)
    driver.find_element(By.ID, '1').find_element(By.CSS_SELECTOR, '.t a').click()
    # driver.find_element(By.ID, "su").click()
    # driver.execute_script("window.open('https://www.taobao.com')")
    # driver.switch_to.window(driver.window_handles[0])
    time.sleep(10)
finally:
    if 'driver' in locals() or 'driver' in globals():
        driver.quit()
