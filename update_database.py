import tv
import sqlite3 as sql

def run_update():
	con=sql.connect("user_data.db")
	cur=con.cursor()
	res=cur.execute("select name from tv_series")
	print(res)
	for i in res:
		print(i)


run_update()