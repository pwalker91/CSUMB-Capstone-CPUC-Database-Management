import matplotlib.pyplot as plt
import sys
import pymysql
import numpy as np
from pylab import *

from PyDB_API import CSDI_MySQL

db = CSDI_MySQL(database = 'testdb', user = 'Moradster', password= 'root')


# connect to MySQL database
db.connect()

# this is the query we will be making
query = """SELECT Speed, date FROM test WHERE date >= "2015-01-03";"""
results = db.select('test', "speed","date", date="2015-01-03", date_operator=">=")
print(results)
x = []
y = []
for records  in results[1]:
    x.append(records[0])
    y.append(records[1])
line, = plt.plot(x, y, 'ko')
title(query)
grid(True)
plt.draw()
plt.show()
F = gcf()
DPI = F.get_dpi()
F.savefig('plot.png', dpi = (80))
#grab results return from the PyDB_MySQL api when a query is executed.
#pandas should only get data to transform meaning results from mysql query