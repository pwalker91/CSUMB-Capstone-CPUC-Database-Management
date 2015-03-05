import matplotlib.pyplot as plt
import pandas
import pymysql
from PyDB_API import CSDI_MySQL

#db = CSDI_MySQL(database = 'testdb', user = 'Moradster', password= 'root')


# connect to MySQL database
conn = pymysql.connect(host="localhost", user="Moradster", passwd="root", db="testdb")


# this is the query we will be making
query = """SELECT Speed, id FROM test WHERE id >= "1" AND id < "9";"""
#db.connect()
#results = db.select('test', "speed","date", date="2015-01-03", date_operator=">=")
#print(results)
df = pandas.read_sql(query, conn, index_col=['id'])
fig, ax = plt.subplots()
df.plot(ax=ax)
# plt.xticks(TimeStamp, (hour))
fig.set_size_inches(20.5,10.5)
plt.grid(True)
plt.draw()
fig.savefig('/Users/Moradster/test2.png', dpi=100)

conn.close()
#grab results return from the PyDB_MySQL api when a query is executed.
#pandas should only get data to transform meaning results from mysql query