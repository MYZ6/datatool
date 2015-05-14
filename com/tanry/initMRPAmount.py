#!/usr/bin/env python
# coding=gbk

#-------------------------
# Copyright (c) 2015
# Tanry Electronic Technology Co., Ltd.
# ChangSha, China
# All Rights Reserved.
# 功能：初始化所有的在途量、已分配量(包括物流中心和央厂)
# 作者：liyzh
# 时间：2015.5.14
#-------------------------

import os 
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'

import cx_Oracle
from config import ipAddr, username, password
# open connection to oracle
conn = cx_Oracle.connect(username + '/' + password + '@' + ipAddr + '/jono')
cursor = conn.cursor()

# 遍历原材料
materailSql = "select m.item_id, c.category_name from JONO.D_T2_ITEM_META m \
    inner join d_t2_item_category c on c.category_id = m.category_id \
    where m.ITEM_TYPE IN ('RAW', 'SEMIS')"
insertSql = insertSql = "insert into JONO.D_T2_MRP_AMOUNT(BRANCH_ID, item_id, ALLOCATION, ON_THE_WAY) \
                values(:1, :2, 0, 0) "

insertArgs = []

def iterateRaw(branchId):
    deleteSql = "delete from D_T2_MRP_AMOUNT t where t.BRANCH_ID = :1"
    # 先删除数据
    cursor.execute(deleteSql, (branchId, ))
    print "delete records ", cursor.rowcount
    
    cursor.execute(materailSql)
    rows = cursor.fetchall()
    for row in rows:
        itemId = row[0]
        insertArgs.append((branchId, itemId))
    

iterateRaw("L00")
iterateRaw("F00")

cursor.executemany(insertSql, insertArgs)
print "insert records ", cursor.rowcount

cursor.execute("commit")

cursor.close()
conn.close()

print('---------------------初始化所有的在途量、已分配量(包括物流中心和央厂)成功！----------------------')
