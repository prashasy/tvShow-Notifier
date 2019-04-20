import sqlite3 as sql

def sql_connect():
	con=sql.connect("user_data.db")
	
	print("Database created successfully")
	cur=con.cursor()
	cur.execute("create table users (id integer primary key,uname text,email text unique)")
	print("Table users created successfully!!")

	cur.execute("create table tv_series (id integer primary key,name text,updates text)")
	print("Table tv_series created successfully!!")

	cur.execute("create table pairs(user_id integer,series_id integer)")

	# tup=['prashasy','prashasy@tiedc.in','game of thrones,west world']
	# cur=con.cursor()
	# try:
	# 	cur.execute("insert into users(name,email)values(?,?)",(tup[0],tup[1]))
	# except:
	# 	print("Error. User exists")
	# print("Data Inserted in users")
	# try:
	# 	cur.execute("select case when exists(select 1 from tv_series where name={?})")
	con.commit()
	con.close()

sql_connect()