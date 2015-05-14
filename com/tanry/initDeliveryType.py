#!/usr/bin/env python
# coding=gbk

#-------------------------
# Copyright (c) 2015
# Tanry Electronic Technology Co., Ltd.
# ChangSha, China
# All Rights Reserved.
# 功能：初始化所有的配送方式数据
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
insertSql = insertSql = "insert into  D_T2_DELIVERY_TYPE(region_id, item_id, delivery_type) \
               VALUES (:1, :2, :3)"

insertArgs = []

deliveryType = "UNIFIED"; # 初始化为统配
def iterateRaw(regionLst):
    placeholderArr = []
    for i in range(1, len(regionLst) + 1):
        placeholderArr.append(":" + str(i))
    placeholders= ', '.join(placeholderArr)
    deleteSql = "delete from D_T2_DELIVERY_TYPE t where t.REGION_ID IN (%s)" % placeholders
#     print deleteSql
    # 清空表
    cursor.execute(deleteSql, regionLst)
    print "delete records ", cursor.rowcount
    
    cursor.execute(materailSql)
    rows = cursor.fetchall()
    for row in rows:
        itemId = row[0]
        for regionId in regionLst:
            insertArgs.append((regionId, itemId, deliveryType))
    
    cursor.executemany(insertSql, insertArgs)
    print "insert records ", cursor.rowcount

regionLst = ["r01", "r02", "r03"]
iterateRaw(regionLst)

cursor.execute("commit")

cursor.close()
conn.close()

print('---------------------初始化所有的配送方式数据成功！----------------------')
