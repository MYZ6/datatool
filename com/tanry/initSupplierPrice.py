#!/usr/bin/env python
# coding=gbk

#-------------------------
# Copyright (c) 2015
# Tanry Electronic Technology Co., Ltd.
# ChangSha, China
# All Rights Reserved.
# 功能：初始化所有的供应商价格数据，要遍历所有原料、价格，相当耗时
# 作者：liyzh
# 时间：2015.5.14
#-------------------------

import os 
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'

import cx_Oracle
# open connection to oracle
conn = cx_Oracle.connect('jono/jono@10.1.1.105/jono')
cursor = conn.cursor()

# 默认使用进货价初始化供应商的价格
priceSql = "SELECT item_price FROM JONO.d_t2_item_price p \
    where p.item_id = :1 and p.price_type = 'PURCHASE'"
def getPurchasePrice(itemId):
#     print itemId, priceSql
    cursor.execute(priceSql, (itemId, )) # 见鬼，这个逗号还非要不可
    # 判断门店、原料与供应商三者的关系数据是否存在，如果不存在，初始化一个值
    row = cursor.fetchone()
    if row == None: # 有一部分原料存在，但是没有采购价（这说明天天与御商的数据并非是大小集关系，而是交集之外各自还存在不同的数据，这可能会引发新的问题）
        return 0
    return row[0]

# 遍历原材料
materailSql = "select m.item_id, c.category_name from JONO.D_T2_ITEM_META m \
    inner join d_t2_item_category c on c.category_id = m.category_id \
    where m.ITEM_TYPE IN ('RAW', 'SEMIS')"
# 判断门店、原料与供应商三者的关系数据是否存在，如果不存在，初始化一个值
selSupplierSql = "SELECT sbi.SUPPLIER_ID FROM D_T2_SUPPLIER_BRANCH_ITEM sbi \
    WHERE sbi.ITEM_ID = :1 AND sbi.BRANCH_ID = :2"
# 如果不存在，初始化一个值
insertSql = "insert into  D_T2_SUPPLIER_BRANCH_ITEM(branch_id, item_id, supplier_id, PRIORITY) values (:1, :2, :3, 0)"
# 初始化供应商价格
insertPriceSql = "insert into JONO.d_t2_item_price(item_id, price_type, supplier_id, item_price, is_current) values(:1, 'SUPPLIER', :2, :3, 1)"


insertArgs = []
insertPriceArgs = []

def scanRelation(itemId, branchId):
    cursor.execute(selSupplierSql, (itemId, branchId))
    # 判断门店、原料与供应商三者的关系数据是否存在，如果不存在，初始化一个值
    rows = cursor.fetchall()
    if rows: # if not empty
        for row in rows:
            supplierId = row[0]
            insertPriceArgs.append((itemId, supplierId, getPurchasePrice(itemId)))
    else:
        # 默认供应商
        supplierId = "1001"
        insertArgs.append((branchId, itemId, supplierId))
#         print itemId
        insertPriceArgs.append((itemId, supplierId, getPurchasePrice(itemId)))

# 清空供应商价格数据，重新装载
cursor.execute("delete from d_t2_item_price where supplier_id is not null")

cursor.execute(materailSql)
rows = cursor.fetchall()
count = 0
for row in rows:
    itemId = row[0]
#     print itemId
    # 更新物流中心的数据
    branchId = "L00"
    scanRelation(itemId, branchId)
    count += 1
    if count % 200 == 0:
        print count # show progress, give hope

# 批量插入关系表数据
cursor.executemany(insertSql, insertArgs)
# 批量插入供应商价格数据
cursor.executemany(insertPriceSql, insertPriceArgs)
cursor.execute("commit")

cursor.close()
conn.close()

print('---------------------初始化所有的供应商价格数据成功！----------------------')
