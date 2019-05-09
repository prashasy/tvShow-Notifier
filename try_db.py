import sqlite3 as sql

con=sql.connect("user_data.db")
cur=con.cursor()

# cur.execute("DELETE from tv_series")
res=cur.execute("select * from tv_series")
for each in res:
	print(each)

con.close()