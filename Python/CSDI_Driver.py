import matplotlib.pyplot as plt
import sys
import pymysql
import numpy as np
from statistics import mean
from pylab import *
from CSDI_MySQL import CSDI_MySQL#talk to them


myDict = {'table':'test', 'type': 'TCP', 'date': 'somedate', 'operator': '>=', 'statistics': 'mean'}

def getData(myDict, *args, **kwargs):
    query = []
    for data in myDict:
        query += "{},".format(data)
    print (query)
#is it possible to write the select statement as a string? and feed the string to CSDI_MySQL?
#