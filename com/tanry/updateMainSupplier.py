#!/usr/bin/env python
# coding=gbk

#-------------------------
# Copyright (c) 2015
# Tanry Electronic Technology Co., Ltd.
# ChangSha, China
# All Rights Reserved.
# 功能：初始化数据时，有的原料存在两个甚至两个以上的主供应商，在这里对数据进行修正
# 作者：liyzh
# 时间：2015.5.8
#-------------------------

import os 
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'

import cx_Oracle
from config import ipAddr, username, password
# open connection to oracle
conn = cx_Oracle.connect(username + '/' + password + '@' + ipAddr + '/jono')
cursor = conn.cursor()

# 遍历原材料，查找出主供应商多于一个的原料-部门
sql = "SELECT sbi.ITEM_ID, sbi.BRANCH_ID, COUNT(*) FROM D_T2_SUPPLIER_BRANCH_ITEM sbi \
    WHERE sbi.PRIORITY = 0 GROUP BY sbi.ITEM_ID, sbi.BRANCH_ID HAVING COUNT(*) >1"
# 获取第一个主供应商（保留为主供应商）
selSql = "SELECT sbi.ITEM_ID, sbi.BRANCH_ID, sbi.SUPPLIER_ID FROM D_T2_SUPPLIER_BRANCH_ITEM sbi \
    WHERE sbi.PRIORITY = 0 AND sbi.ITEM_ID = :1 AND sbi.BRANCH_ID = :2"
# 除第一个主供应商，去除掉其它供应商的主属性
updateSql = "update D_T2_SUPPLIER_BRANCH_ITEM sbi set sbi.PRIORITY = 1 \
    where sbi.ITEM_ID = :1 and sbi.BRANCH_ID = :2 and sbi.SUPPLIER_ID ! = :3"

updateArgs = []

cursor.execute(sql)
rows = cursor.fetchall()
count = 0
for row in rows:
    itemId = row[0]
    branchId = row[1]
    count += 1
    if count % 200 == 0:
        print count # show progress, give hope
    cursor.execute(selSql, (itemId, branchId))
    # 获取第一个主供应商（保留为主供应商）
    row1 = cursor.fetchone()
#     print row1
    updateArgs.append(row1)

# 批量更新
cursor.executemany(updateSql, updateArgs)
print "update records ", cursor.rowcount
cursor.execute("commit")

cursor.close()
conn.close()

print('---------------------修正主供应商数据成功！----------------------')

