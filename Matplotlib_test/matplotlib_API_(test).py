import matplotlib.pyplot as plt
import pandas
import pymysql


# connect to MySQL database
conn = pymysql.connect(host="localhost", user="Moradster", passwd="root", db="testdb")


# this is the query we will be making
query = """
    SELECT Speed, Date
    FROM
    WHERE Data >= "2015-01-03"
    AND Data < "2015-02-25";
    """

df = pandas.read_sql(query, conn, index_col=['Data'])
fig, ax = plt.subplots()
df.plot(ax=ax)
conn.close()