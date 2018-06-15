# -*- coding: utf-8 -*-

import sys, os, urllib2, threading, time, re
from selenium import webdriver

from selenium.common.exceptions import NoSuchElementException

reload(sys)
sys.setdefaultencoding('utf-8')


class Grab2:
    def __init__(self, url):
        """
        Grab init
        :param url: URL
        """
        self.url = url

    @classmethod
    def open_content(cls, url):
        browser = webdriver.Firefox()
        browser.implicitly_wait(10)  # seconds
        browser.get(url)

        print "1"

    @classmethod
    def pull_down(cls, driver, ele):
        count = 0
        while not cls.is_exists(driver, ele):
            js = "window.scrollTo(0,document.body.scrollHeight-" + str(count * count * 200) + ")"
            driver.execute_script(js)
            count = count + 1

    @classmethod
    def is_exists(cls, driver, ele):
        try:
            driver.find_element_by_css_selector(ele)
        except NoSuchElementException:
            return False
        return True
