#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wangrong'
import yaml, os
import paramiko


class check_midware():
    def __init__(self, midware_cfg='midware.lst'):
        basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        midware_cfg_path = os.path.join(basedir, 'conf', midware_cfg)
        with open(midware_cfg_path, 'r') as f:
            cont = f.read()
            self.midware_info = yaml.load(cont)

    def connect_to_server(self, host_info):
        ''' host_info=172.16.80.44:root:1jian8Shu!'''
        try:
            host_ip = host_info.split(':')[0]
            host_user = host_info.split(':')[1]
            host_passwd = host_info.split(':')[2]
        except Exception as err:
            print(err)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(host_ip, 22, host_user, host_passwd, timeout=3)
            return ssh
        except Exception as err:
            print(err)

    def check_zmq(self):
        ret_code=True
        zmq_info = self.midware_info['zmq']
        zmq_host_info = zmq_info['host_info']
        zmq_install_dir = zmq_info['zmq_install_dir']
        for one_zmq_info in zmq_host_info:
            ssh_instance = self.connect_to_server(one_zmq_info)
            check_cmd = 'ps -ef|grep zmq|grep -v grep | grep "{}"|wc -l'.format(zmq_install_dir)
            stdin, stdout, stderr = ssh_instance.exec_command(check_cmd)
            output = stdout.read()
            if int(output):
                print("[{}]zmq process is running".format(one_zmq_info.split(":")[0]))
            else:
                print("[{}]zmq process is stoped".format(one_zmq_info.split(":")[0]))
                ret_code = False
            ssh_instance.close()
        return ret_code

    def check_zk(self):
        ret_code = True
        zk_info = self.midware_info['zookeeper']
        zk_host_info = zk_info['host_info']
        zk_install_dir = zk_info['zk_install_dir']
        for one_zk_info in zk_host_info:
            ssh_instance = self.connect_to_server(one_zk_info)
            check_cmd = 'ps -ef|grep zookeeper|grep -v grep | grep "{}"|wc -l'.format(zk_install_dir)
            stdin, stdout, stderr = ssh_instance.exec_command(check_cmd)
            output = stdout.read()
            if int(output):
                print("zookeeper process is running")
            else:
                print("zookeeper process is stoped")
                ret_code = False
            ssh_instance.close()
        return ret_code

    def check_zcache(self):
        ret_code = True
        zache_info = self.midware_info['zcache']
        zcache_host_info = zache_info['host_info']
        zcache_install_dir = zache_info['zcache_install_dir']
        for one_zcache_info in zcache_host_info:
            ssh_instance = self.connect_to_server(one_zcache_info)
            check_cmd = 'ps -ef|grep zcache|grep -v grep|grep redis-server | grep "{}"|wc -l'.format(zcache_install_dir)
            stdin, stdout, stderr = ssh_instance.exec_command(check_cmd)
            output = stdout.read()
            if int(output):
                print("[{}]zcache process is running".format(one_zcache_info.split(":")[0]))
            else:
                print("[{}]zcache process is stoped".format(one_zcache_info.split(":")[0]))
                ret_code = False
            ssh_instance.close()
        return ret_code


if __name__ == '__main__':
    c = check_midware()
    c.check_zk()
