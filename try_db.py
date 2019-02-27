import sqlite3 as sql

def sql_connect():
	con=sql.connect("user_data.db")
	
	print("Database created successfully")
	cur=con.cursor()
	cur.execute("create table users (id integer primary key,name text,email text unique,date real)")
	print("Table users created successfully!!")
	cur.execute("create table tv_series (id integer primary key,name text)")
	print("Table tv_series created successfully!!")
	cur.execute("create table pairs(user_id integer,series_id integer)")





	con.close()

sql_connect()