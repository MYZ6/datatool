#!/usr/bin/env python
#coding=gbk

#-------------------------
# Copyright (c) 2014
# Tanry Electronic Technology Co., Ltd.
# ChangSha, China
# All Rights Reserved.
# ���ܣ�ִ��sql�ű��ļ�
# ���ߣ�lyz
# ʱ�䣺2015.6.9
#-------------------------

import os
import time
import datetime
import cx_Oracle

#set chinese encoding
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'

#open connection to oracle
conn = cx_Oracle.connect('jono/jono@10.1.1.105/jono')
cursor = conn.cursor()


start = time.clock()
f = open("inout2.sql", 'r')
lines = f.readlines()
param = []
i = 0
for line in lines:
#     if i % 300 == 0 and i > 0:
#         print i
    cursor.execute(line[:-2])
    i += 1
f.close()


end = time.clock()
print end-start
cursor.execute("commit")

cursor.close()
conn.close()

print('******************�������ݵ��붼�Ѿ����*******************')
