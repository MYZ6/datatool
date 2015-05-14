#!/usr/bin/env python
# coding=utf-8

#-------------------------
# Copyright (c) 2015
# Tanry Electronic Technology Co., Ltd.
# ChangSha, China
# All Rights Reserved.
# 功能：初始化所有的配送单位、配方单位、超收率等数据
# 作者：liyzh
# 时间：2015.5.14
#-------------------------

import os 
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'

import cx_Oracle
# open connection to oracle
conn = cx_Oracle.connect('jono/jono@10.1.1.105/jono')
cursor = conn.cursor()

# 遍历原材料
materailSql = "select m.item_id, item_dimension, c.category_name from JONO.D_T2_ITEM_META m \
    inner join d_t2_item_category c on c.category_id = m.category_id \
    where m.ITEM_TYPE IN ('RAW', 'SEMIS')"
insertSql = insertSql = "INSERT INTO D_T2_DELIVERY_UNIT (ITEM_ID, DELIVERY_UNIT, DELIVERY_FACTOR, RECIPE_UNIT, RECIPE_FACTOR, UNIT_VOLUME, UNIT_WEIGHT, OUT_RECEIVE_RATE) \
               VALUES (:1, :2, 1, :3, 1, 1, 100, 1.3)"

insertArgs = []

# 清空表
cursor.execute("truncate table D_T2_DELIVERY_UNIT")

cursor.execute(materailSql)
rows = cursor.fetchall()
count = 0
for row in rows:
    itemId = row[0]
    itemDimension = row[1]
    insertArgs.append((itemId, itemDimension, itemDimension))

cursor.executemany(insertSql, insertArgs)
cursor.execute("commit")

cursor.close()
conn.close()

print('---------------------初始化所有的供应商价格数据成功！----------------------')
