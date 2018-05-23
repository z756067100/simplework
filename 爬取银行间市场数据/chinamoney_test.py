# -*- coding: utf-8 -*-
"""
Created on Mon Apr 09 00:40:29 2018

@author: hasee
"""
import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from sqlalchemy import create_engine

import pandas as pd
import time
import datetime
import os
import re

if __name__ == '__main__':
#     db_info = {'user': 'root',
#                'password': 'root',
#                'host': 'localhost',
#                'port': 3306}
#     engine = create_engine('mysql+mysqlconnector://%(user)s:%(password)s@%(host)s:%(port)s' % db_info)
#     conn = engine.connect()
#     temp = pd.read_sql('SELECT publish, url FROM spider_share.chinabond order by publish DESC limit 12', conn)
#     url_list = temp['url'].tolist()
#     sql_query = "INSERT INTO spider_share.chinabond VALUES ('%s', '%s', '%s')"
#     print 'START'

     options = webdriver.ChromeOptions()
     cur_dir = os.path.dirname(os.path.abspath(__file__))
     prefs = {"download.default_directory": cur_dir,
              "profile.managed_default_content_settings.images":2}
     options.add_experimental_option("prefs", prefs)
     driver = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"
     browser = webdriver.Chrome(executable_path=driver, chrome_options=options, service_args=['--ignore-ssl-errors=true'])
#     def browser_conn():
#         driver = r"D:\phantomjs-2.1.1-windows\bin\phantomjs.exe"
#         dcap = dict(DesiredCapabilities.PHANTOMJS)
#         dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36')
#         browser = webdriver.PhantomJS(executable_path=driver, service_args=['--ignore-ssl-errors=true', '--load-images=no'])
#         browser.set_page_load_timeout(10)
#         browser.implicitly_wait(30)
#         return browser
#
#     browser = browser_conn()

     url_home = 'http://www.chinamoney.com.cn/fe/Channel/5410'

    # # 政策性银行债
#     browser.find_element_by_css_selector('span[id=span_21630]').click()
     while True:
        print 'sleep'
        time.sleep(10)
        print '%s' % datetime.datetime.now()
        print 'get_url...'
        is_connected = False
        while not is_connected:
            try:
                browser.get(url_home)
                is_connected = True
            except TimeoutException, m:
                print 'timeout'
                browser.close()
                browser = browser_conn()
        # browser.find_element_by_css_selector('a[id=a_289536]').click()
        # 全部
        print 'get_result_list'
        title_list=[]
        browser.switch_to_frame("iframe00004")
        count=0
        while title_list==[] and count<10:
            result_list = browser.find_element_by_css_selector('ul#data-service-guide')
            print result_list
            title_list = result_list.find_elements_by_css_selector('a[style]')
            print title_list
            publish_list = result_list.find_elements_by_css_selector('span')
            print publish_list
            count+=1
#        a=title_list[0]
#        print a
#        b=a.get_attribute('title')
#        print b
#        b.decode
        for t, p in zip(title_list, publish_list):
            title = t.get_attribute('title')
            url = t.get_attribute('href')
            print url
            publish = p.text
            # 如果出现相同url，则跳出循环
#            if url in url_list:
#                continue
#            url_list.append(url)
            print '%s %s' % (publish, title)
#            conn = engine.connect()
#            conn.execute(sql_query % (publish, title, url))
#            send_emails(['756067100@qq.com'], title, url, [])
#            send_emails(['242388500@qq.com', '2251228903@qq.com', '393355844@qq.com'], title, url, [])
        browser.switch_to.default_content()
    # browser.quit()
     print 'END'
