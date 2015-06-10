#!/usr/bin/env python
#coding=gbk

#-------------------------
# Copyright (c) 2014
# Tanry Electronic Technology Co., Ltd.
# ChangSha, China
# All Rights Reserved.
# 功能：构造insert all语句，加快执行速度，提升20倍
# 作者：lyz
# 时间：2015.6.9
#-------------------------

import os
import time
import cx_Oracle

#set chinese encoding
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'


#open connection to oracle
conn = cx_Oracle.connect('jono/jono@10.1.1.105/jono')
cursor = conn.cursor()

def insertAll(fileName):
    f = open(fileName, 'r')
    lines = f.readlines()
    i = 0
    all_sql = []
    new_sql = "insert all "
    for line in lines:
    #构建insert all
        if i % 300 == 0 and i > 0:
            new_sql += " select 1 from dual"
            all_sql.append(new_sql)
    #         print new_sql
            new_sql = "insert all "
    #         print i
        trim_sql = line[7:-2]
    #     print trim_sql
        new_sql += trim_sql + " "
        i += 1
    f.close()
    
    # handle tail data
    if (i - 1) % 300 != 0:
        new_sql += " select 1 from dual"
        all_sql.append(new_sql)
    
    print len(all_sql)
    # print all_sql
    
    start = time.clock()
    for sql in all_sql:
    #     print time.clock()
        cursor.execute(sql)
    
    end = time.clock()
    print fileName + " : " + str(end-start)
    cursor.execute("commit")

# insertAll("cdetail.sql")
insertAll("storage.sql")

cursor.close()
conn.close()

print('******************所有数据导入都已经完成*******************')
