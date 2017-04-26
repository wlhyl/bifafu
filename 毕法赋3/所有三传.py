#!/usr/bin/python3
from prettytable import PrettyTable
from ganzhiwuxin import *
from shipan import *

所有天盘=[]
for i in range(1, 13):
    a = 天盘(支(i), 支(1))
    所有天盘.append(a)

所有甲子 = []
for i in range(1, 11):
    for j in range(1, 13):
        if 阴阳相同(干(i), 支(j)):
            所有甲子.append(干支(干(i), 支(j)))

所有栻盘 = []
for i in 所有天盘:
    for j in 所有甲子:
        所有栻盘.append(栻盘(i, j))

result = []
for i in 所有栻盘:
    if i.三传 not in result:
        result.append(i.三传)

print(len(result))
for i in result:
    print(i)
    print()
