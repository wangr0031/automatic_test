#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wangrong'
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains ##鼠标事件 右键，悬停，拖拽，左键单击
'''
perform() 执行所有ActionChains中的行为
move_to_element() 鼠标悬停
'''
from time import sleep

class WebTest():
    def __init__(self, web_url):
        # self.url = "http://172.16.80.3/portal-web/#"
        self.url = web_url
        self.chrome_driver = webdriver.Chrome()
        self.wait = ui.WebDriverWait(self.chrome_driver, 10)
        try:
            self.chrome_driver.get(self.url)
            print("Open Chrome browser Success, Access website Title:{} URL:{}".format(self.chrome_driver.title,
                                                                                       self.chrome_driver.current_url))
        except Exception as err:
            print("Open Chrome Failed:{}".format(err))

    def login_web(self, username, password):
        try:
            self.wait.until(lambda driver: driver.find_element_by_xpath(
                "//div[@class='form-group has-feedback']/input[@name='userCode']"))

            self.chrome_driver.find_element_by_xpath(
                "//div[@class='form-group has-feedback']/input[@name='userCode']").send_keys(
                username)
            self.wait.until(lambda driver: driver.find_element_by_xpath(
                "//div[@class='form-group has-feedback']/input[@name='password']"))
            self.chrome_driver.find_element_by_xpath(
                "//div[@class='form-group has-feedback']/input[@name='password']").click()
            self.chrome_driver.find_element_by_xpath(
                "//div[@class='form-group has-feedback']/input[@name='password']").send_keys(
                password)
            self.chrome_driver.find_element_by_xpath("//div[@class='form-group']/button[@type='button']").click()
            sleep(2)
        except Exception as err:
            print("Login Web Failed")

    def is_login(self):
        try:
            text=self.chrome_driver.find_element_by_xpath("//*[@id='portalMainHeader']/div/div[2]/div/div[1]/input").text
            print("Login success")
            #self.chrome_driver.quit()
        except Exception as err:
            print("Login Failed")

    def close_chrome(self):
        self.chrome_driver.quit()

if __name__ == '__main__':
    w=WebTest('http://172.16.80.3/portal-web')
    w.login_web('admin','123')
    w.is_login()