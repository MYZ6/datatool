#!/usr/bin/env python
# coding=gbk

#-------------------------
# Copyright (c) 2015
# Tanry Electronic Technology Co., Ltd.
# ChangSha, China
# All Rights Reserved.
# 功能：添加供货周期和生产周期（自己造的虚拟数据）
# 作者：liyzh
# 时间：2015.5.18
#-------------------------

import os 
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'

import random
import cx_Oracle
from config import ipAddr, username, password
# open connection to oracle
conn = cx_Oracle.connect(username + '/' + password + '@' + ipAddr + '/jono')
cursor = conn.cursor()


print('---------------供货周期信息--------------------')
cursor.execute("truncate table d_t2_supply_cycle")

materailSql = "select m.item_id from JONO.D_T2_ITEM_META m where m.ITEM_TYPE IN ('RAW', 'SEMIS')"
cursor.execute(materailSql)
rows = cursor.fetchall()
insertArgs = []
for row in rows:
    itemId = row[0]
    cycle = random.randint(0, 5)
    insertArgs.append(('L00', itemId, cycle))
    insertArgs.append(('F00', itemId, cycle))
insertSql = "INSERT INTO D_T2_SUPPLY_CYCLE (BRANCH_ID, ITEM_ID, SUPPLY_CYCLE) \
               VALUES (:1, :2, :3)"
cursor.executemany(insertSql, insertArgs)     

  
print('-----------------半成品生产周期表-----------------')
cursor.execute("truncate table d_t2_production_cycle")

semisSql = "SELECT m.item_id FROM JONO.D_T2_ITEM_META m \
    LEFT JOIN JONO.D_T2_ITEM_CATEGORY c ON c.CATEGORY_ID = m.CATEGORY_ID \
    WHERE c.ITEM_TYPE IN ( 'SEMIS')"
cursor.execute(semisSql)
rows = cursor.fetchall()
insertArgs = []
for row in rows:
    itemId = row[0]
    cycle = random.randint(0, 5)
    insertArgs.append(('F00', itemId, cycle))

insertSql = "INSERT INTO D_T2_PRODUCTION_CYCLE (BRANCH_ID, ITEM_ID, PRODUCTION_CYCLE) \
               VALUES (:1, :2, :3)"
cursor.executemany(insertSql, insertArgs)               
    
    
cursor.execute("commit")
cursor.close()
conn.close()

print('---------------------添加供货周期和生产周期（自己造的虚拟数据）成功！----------------------')