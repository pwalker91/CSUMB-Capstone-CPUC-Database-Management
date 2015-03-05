import matplotlib.pyplot as plt
import pandas
import pymysql


# connect to MySQL database
conn = pymysql.connect(host="localhost", user="Moradster", passwd="root", db="testdb")


# this is the query we will be making
query = """SELECT Speed, Date FROM test WHERE Date >= "2015-01-03" AND Date < "2015-02-25";"""

df = pandas.read_sql(query, conn, index_col=['Date'])
fig, ax = plt.subplots()
df.plot(ax=ax)
# plt.xticks(TimeStamp, (hour))
fig.set_size_inches(20.5,10.5)
plt.grid(True)
plt.draw()
fig.savefig('/Users/Moradster/test2.png', dpi=100)

conn.close()
