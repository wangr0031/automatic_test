#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wangrong'

import unittest
import os
from unit_module.check_ip import check_ip
from unit_module.check_db import check_db
from unit_module.check_midware import check_midware
from unit_module.check_web import check_web
from HTMLTestRunner_PY3 import HTMLTestRunner


class serverTest(unittest.TestCase):
    def setUp(self):
        print("开始机器连通性测试...")

    def test_connection(self):
        tconnect = check_ip()
        res = tconnect.check_ipaddress()
        self.assertEqual(res, 0)

    def tearDown(self):
        print("测试结束...")


class databaseTest(unittest.TestCase):
    def setUp(self):
        print("开始数据库测试...")

    def test_databse_login(self):
        dbconnect = check_db()
        res = dbconnect.access_db()
        self.assertTrue(res)

    def test_db_usages_rate(self):
        dbconnect = check_db()
        res = dbconnect.db_usages_rate()
        self.assertTrue(res)

    def tearDown(self):
        print("测试结束...")


class midwareTest(unittest.TestCase):
    def setUp(self):
        print("开始中间件测试...")

    def test_zk_process(self):
        midconnect = check_midware()
        res = midconnect.check_zk()
        self.assertTrue(res)

    def test_zmq_process(self):
        midconnect = check_midware()
        res = midconnect.check_zmq()
        self.assertTrue(res)

    def test_zcache_process(self):
        midconnect = check_midware()
        res = midconnect.check_zcache()
        self.assertTrue(res)

    def tearDown(self):
        print("测试结束...")


if __name__ == '__main__':
    import test_unit_cfg as test_unit
    import datetime

    basedir = os.path.dirname(os.path.abspath(__file__))
    report = os.path.join(basedir, 'data', 'test_report_{}.html'.format(datetime.datetime.now().strftime('%Y-%m-%d')))
    all_test_unit = test_unit.test_list
    st = unittest.TestSuite()
    # report = os.path.join('C:/Users/cc/Desktop/20180905/测试报告.html')
    st.addTests(all_test_unit)
    with open(report, 'wb') as f:
        runner = HTMLTestRunner(f, verbosity=2, title='部署完成-测试报告', description='执行人：python脚本')
        runner.run(st)
