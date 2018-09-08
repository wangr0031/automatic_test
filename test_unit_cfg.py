#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wangrong'
from main_unittest_interface import *

test_list = [serverTest('test_connection'), databaseTest('test_databse_login'), databaseTest('test_db_usages_rate'),
             midwareTest('test_zk_process'), midwareTest('test_zmq_process'), midwareTest('test_zcache_process')]
