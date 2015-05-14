#!/usr/bin/env python
# coding=gbk

#-------------------------
# Copyright (c) 2015
# Tanry Electronic Technology Co., Ltd.
# ChangSha, China
# All Rights Reserved.
# 功能：每个库位初始化一百五十个原料，大概二十个库位，三千个原料（包括半成品）
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

def formatSerial(serialNum):
    serial = str(serialNum);
    addLength = 3 - len(serial) # 补齐三位数编码
    i = 0
    while i < addLength:
        serial = "0" + serial
        i += 1
    return serial

# 遍历原材料
materailSql = "select m.item_id, c.category_name from JONO.D_T2_ITEM_META m \
    inner join d_t2_item_category c on c.category_id = m.category_id \
    where m.ITEM_TYPE IN ('RAW', 'SEMIS')"
insertSql = insertSql = "INSERT INTO D_T2_SHELF_ITEM (SHELF_ID, ITEM_ID, PRIORITY) \
             VALUES (:1, :2, 0)"

insertArgs = []

# 清空表
cursor.execute("truncate table D_T2_SHELF_ITEM")

cursor.execute(materailSql)
rows = cursor.fetchall()
count = 0
shelfCount = 1
shelfId = "001"
for row in rows:
    itemId = row[0]
    if count % 150 == 0: # 每个库位初始化一百五十个原料
        shelfCount += 1
        shelfId = formatSerial(shelfCount)
    insertArgs.append((shelfId, itemId))
    count += 1

cursor.executemany(insertSql, insertArgs)
cursor.execute("commit")

cursor.close()
conn.close()

print('---------------------每个库位初始化一百五十个原料数据成功！----------------------')
