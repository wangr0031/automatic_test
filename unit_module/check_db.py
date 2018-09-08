#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wangrong'

import os, sys
import re
import cx_Oracle


class check_db():
    def __init__(self, db_cfg='db.lst'):
        # 数据库连通性测试
        self.db_info_list = list()
        basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_cfg_path = os.path.join(basedir, 'conf', db_cfg)
        with open(db_cfg_path) as f:
            for one in f:
                if one.startswith('#'):
                    continue
                self.db_info_list.append(one.strip())

    def access_db(self):
        res_code = True
        for one in self.db_info_list:
            dbtype = one.split(":")[0]
            if re.search('ora', dbtype.lower()):
                dbipaddress = one.split(":")[1]
                dblisten_port = one.split(":")[2]
                dbservice_name = one.split(":")[3]
                dbuser = one.split(":")[4]
                dbpasswd = one.split(":")[5]
                res = self.access_db_oracle(dbuser, dbpasswd, dbipaddress, dblisten_port, dbservice_name)
                if not res:
                    res_code = False
            elif re.search('mysql', dbtype.lower()):
                res = self.access_db_mysql()
                if res:
                    print("access Mysql database success ")
                else:
                    print("access Mysql database failed ")
                    res_code = False
        return res_code

    def access_db_oracle(self, username, password, dbip, db_port, db_servicename):
        res_code = True
        try:
            db_dsn = cx_Oracle.makedsn(dbip, db_port, db_servicename)
            ora_con = cx_Oracle.connect(username, password, db_dsn)
            print("access Oracle database {} success".format(db_dsn))
            ora_con.close()
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            print("access Oracle database failed,reason:{}".format(error.message))
            res_code = False
        return res_code

    def access_db_mysql(self):
        res_code = True
        return res_code

    def db_usages_rate(self):
        res_code = True
        for one in self.db_info_list:
            if one.split(":")[-1].lower() != 'dba':
                continue
            dbtype = one.split(":")[0]
            if re.search('ora', dbtype.lower()):
                dbipaddress = one.split(":")[1]
                dblisten_port = one.split(":")[2]
                dbservice_name = one.split(":")[3]
                dbuser = one.split(":")[4]
                dbpasswd = one.split(":")[5]
                res = self.db_usages_rate_by_oracle(dbuser, dbpasswd, dbipaddress, dblisten_port, dbservice_name)
                if not res:
                    res_code = False
            elif re.search('mysql', dbtype.lower()):
                res = self.db_usages_rate_by_mysql()
                if res:
                    print("Mysql database [{}] tablespace usages is ok".format('dd'))
                else:
                    res_code = False
                    print("Mysql database [{}] tablespace usages in problem".format('dd'))

        return res_code

    def db_usages_rate_by_oracle(self, username, password, dbip, db_port, db_servicename):
        res_code = True
        try:
            db_dsn = cx_Oracle.makedsn(dbip, db_port, db_servicename)
            ora_con = cx_Oracle.connect(username, password, db_dsn)
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            print("access Oracle database failed,reason:{}".format(error.message))
            res_code = False
            return res_code
        sqlquery = '''
        SELECT a.tablespace_name,
       round(total / 1024 / 1024 / 1024,2) Total,
       round(free / 1024 / 1024 / 1024,2) free,
       round((total - free) / 1024 / 1024 / 1024,2) Used,
       ROUND((total - free) / total, 4) * 100 "Usage rate%"
  FROM (SELECT tablespace_name, SUM(bytes) free
          FROM DBA_FREE_SPACE
         GROUP BY tablespace_name) a,
       (SELECT tablespace_name, SUM(bytes) total
          FROM DBA_DATA_FILES
         GROUP BY tablespace_name) b
 WHERE a.tablespace_name = b.tablespace_name
        '''
        cursor = ora_con.cursor()
        try:
            result = cursor.execute(sqlquery)
            # for i in result:
            #     print (i)
            wan_res = self.warning_tablespace_usages_from_oracle(result)
            if wan_res:
                print("database tablespace usage is ok")
            else:
                res_code = False
                return res_code
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            print("query tablespace usage failed,reason:{}".format(error.message))
            res_code = False
            return res_code
        return res_code

    def db_usages_rate_by_mysql(self):
        pass

    def warning_tablespace_usages_from_oracle(self, result, warning_rate=95,
                                              exclude_tablespace=['UNDO', 'SYSAUX', 'TEMP', 'SYSTEM', 'SYS']):
        for onerow in result:
            tablespace_name = onerow[0]
            #print (onerow[0],onerow[4])
            if tablespace_name in exclude_tablespace:
                continue
            usage_rate = onerow[4]
            if usage_rate > warning_rate:
                print("database tablespace [{}] usage in problem,total:{},used:{},usage_rate:{}".format(
                    tablespace_name, onerow[1], onerow[3], usage_rate))
                return False
        return True


if __name__ == '__main__':
    c = check_db()
    #c.access_db()
    c.db_usages_rate()
