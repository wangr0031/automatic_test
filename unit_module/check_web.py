#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wangrong'

import yaml
from selenium import webdriver
import os, re


class check_web():
    def __init__(self, web_cfg='web.lst'):
        basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        midware_cfg_path = os.path.join(basedir, 'conf', web_cfg)
        with open(midware_cfg_path, 'r') as f:
            cont = f.read()
            self.web_info = yaml.load(cont)
        dr_type = self.web_info['web_driver']
        if dr_type.upper() == 'CHROME':
            self.dr = webdriver.Chrome()
            print("open Chrome browser Success!")
        elif dr_type.upper() == 'FIREFOX':
            self.dr = webdriver.Firefox()
            print("open Chrome browser Success!")
        else:
            print("Unknow browser")

    def open_web(self):
        res_code = True
        all_web_url = self.web_info['web_url']
        if isinstance(all_web_url, str):
            retcode = self.access_web(all_web_url)
            if not retcode:
                res_code = False
        elif isinstance(all_web_url, list):
            for one_url in all_web_url:
                retcode = self.access_web(one_url)
            if not retcode:
                res_code = False
        return res_code

    def access_web(self, url):
        res_code = True
        try:
            self.dr.get(url)
            web_title = self.dr.title
            web_url = self.dr.current_url
            print('access website success! Url:[{}], Title:[{}]'.format(web_url, web_title))
        except Exception as err:
            res_code = False
            print('access website failed! Url:[{}]'.format(url))
            print('Error:', err)
        return res_code

    def close_browser(self):
        self.dr.close()

    def login_web(self):
        res_code=True
        try:
            self.input_value_by_name(self.web_info['web_login']['username_ele_by_name'],
                                     self.web_info['web_login']['username'])
            self.input_value_by_name(self.web_info['web_login']['password_ele_by_name'],
                                     self.web_info['web_login']['password'])
            self.input_value_by_xpath(self.web_info['web_login']['login_ele_by_xpath'])
            res_value=self.get_value_by_xpath(self.web_info['web_login']['is_login_ele_by_xpath'])
            if res_value == self.web_info['web_login']['is_login_value']:
                res_code=True
            else:
                res_code=False
        except Exception as err:
            res_code = False
            print("login to web failed,error:{}".format(err))
        return res_code

    def input_value_by_name(self, name, value=None):
        self.dr.implicitly_wait(10)
        if value is None:
            self.dr.find_element_by_name(name).click()
        else:
            self.dr.find_element_by_name(name).clear()
            self.dr.find_element_by_name(name).send_keys(value)

    def input_value_by_xpath(self, xpath_name, value=None):
        self.dr.implicitly_wait(10)
        if value is None:
            self.dr.find_element_by_xpath(xpath_name).click()
        else:
            self.dr.find_element_by_xpath(xpath_name).clear()
            self.dr.find_element_by_xpath(xpath_name).send_keys(value)

    def get_value_by_xpath(self,xpath_name):
        self.dr.implicitly_wait(10)
        get_value=self.dr.find_element_by_xpath(xpath_name).text
        return get_value


if __name__ == '__main__':
    c = check_web()
    c.open_web()
    c.login_web()
