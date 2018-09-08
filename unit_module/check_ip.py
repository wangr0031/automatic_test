#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wangrong'

import paramiko
import os


class check_ip():
    def __init__(self, ip_cfg='ip.lst'):
        basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.ip_cfg_path = os.path.join(basedir, 'conf', ip_cfg)

    def check_ipaddress(self):
        rescode=0
        with open(self.ip_cfg_path) as f:
            for one in f:
                one=one.strip()
                if one.startswith('#'):
                    continue
                try:
                    host=one.split(':')[0]
                    user=one.split(':')[1]
                    passwd=one.split(':')[2]
                except Exception as e1:
                    rescode=-1
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    ssh.connect(host,22, user, passwd,timeout=3)
                    print ("connect server:{} success".format(host))
                except Exception as e2:
                    print ("connect server:{} failed".format(host))
                    rescode=-1
            return rescode


if __name__ == '__main__':
    c=check_ip()
    res=c.check_ipaddress()
    print (res)