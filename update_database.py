import tv
import sqlite3 as sql

def run_update():
	con=sql.connect("user_data.db")
	cur=con.cursor()
	try:
		res=cur.execute("select name from tv_series")
		m=""
		for item in res:
			m+="TV Series: "+item +"\n" +"Status: "+tv.imdb_data(item)+"\n\n"
			try:
				result=cur.execute("insert into tv_series(updates) values(?)",(m,))
			except:
				print("Error inserting data for {}".format("item"))
	except:
		print("Error finding names of series")
run_update()