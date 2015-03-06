import matplotlib.pyplot as plt
import sys
import pymysql
import numpy as np
from pylab import *
from PyDB_API import CSDI_MySQL

def plotGraph():
    
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

def lineGraph():
    query = """SELECT Speed, id FROM test WHERE id >= "1";"""
    results = db.select('test', "speed","id", id="0", id_operator=">")
    print (results)
    x = []
    y = []
    for records in results[1]:
        x.append(records[0])
        y.append(records[1])
    plt.plot(y, x)
    title(query)
    grid(True)
    plt.draw()
    plt.show()
    F = gcf()
    DPI = F.get_dpi()
    F.savefig('line.png', dpi = (80))

def barGraph():
    count = 0
    query = """SELECT Speed, id FROM test WHERE id >= "0" and ;"""
    results = db.select('test', "speed","id", id="0", id_operator=">")
    print (results)
    x = []
    y = []
    for records in results[1]:
        x.append(records[0])
        y.append(records[1])
    print (x)
    N = 12
    fig, ax = plt.subplots()
    ind = np.arange(N)
    #print(ind)
    rects = ax.bar(ind, x, .35, color = 'r')
    ax.set_ylabel('speed')
    ax.set_title('Speed by ID')
    ax.set_xticks(ind+.35)
    ax.set_xticklabels(y)
    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')
    plt.show()
    F = gcf()
    DPI = F.get_dpi()
    F.savefig('bar.png', dpi = (80))




db = CSDI_MySQL(database = 'testdb', user = 'Moradster', password= 'root')


# connect to MySQL database
db.connect()
#lineGraph()
barGraph()

