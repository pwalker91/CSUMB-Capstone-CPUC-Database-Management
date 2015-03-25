import sys
import json
from CSDI_MySQL import CSDI_MySQL#talk to them
#from CSDI_matplotlib_adv.py import CSDI_MPL as mpl
myDict = {'table':'test','criteria':{ 'date': '2015-1-23','date_operator': '>='},'statistics':'mean'}

#results = db.select(myDict['table']+"Results", **myDict['criteria'])
db = CSDI_MySQL(database = 'testdb', user = 'Moradster', password= 'root')
print (**myDict['criteria'])
#results = db.select(myDict['table'])
print (results)