import tv
import sqlite3 as sql

def run_update():
	con=sql.connect("user_data.db")
	cur=con.cursor()
	try:
		res=cur.execute("select name from tv_series")
		m=""
		for item in res:
			print(item[0])
			m+="TV Series: "+item[0] +"\n" +"Status: "+tv.imdb_data(item[0])+"\n\n"
			print(m)
			try:
				temp=item[0]
				result=cur.execute("update tv_series set updates=? where name=?",(m,temp))
				print("Database Updated for: "+item[0])
			except sql.Error as e:
				print("Error inserting data for {}".format(item[0]))
				print("Error->"+e)
	except:
		print("Error finding names of series")
run_update()