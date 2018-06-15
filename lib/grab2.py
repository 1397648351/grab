# -*- coding: utf-8 -*-

import sys, os, urllib2, threading, time, re
from selenium import webdriver
from pyquery import PyQuery as pq

from selenium.common.exceptions import NoSuchElementException

reload(sys)
sys.setdefaultencoding('utf-8')


class Grab2:
    driver = webdriver.Firefox()

    def __init__(self, url):
        """
        Grab init
        :param url: URL
        """
        self.url = url

    @classmethod
    def open_content(cls, url):
        try:
            cls.driver.get(url)
            element = cls.driver.find_element_by_id("yc")
            element.click()
            element = cls.driver.find_element_by_id("zkzj")
            while element.text != '点击关闭':
                time.sleep(0.1)
            html = cls.driver.page_source.decode('utf-8', 'ignore')
            doc = pq(html)
            list_chapter = doc('#detaillist ul li').items()
            chapters = []
            index = 0
            for chapter in list_chapter:
                index = index + 1
                title = chapter('a').text()
                href = chapter('a').attr('href')
                chapters.append({
                    'index': index,
                    'title': title,
                    'href': href
                })
            print chapters[0]['title']
        finally:
            cls.driver.close()

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
