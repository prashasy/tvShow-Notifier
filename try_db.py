import sqlite3 as sql

con=sql.connect("user_data.db")
cur=con.cursor()




#INSERT
# series="suits"
# res=cur.execute("insert into tv_series(name) values(?)",(series,))



name="Prashasy"
email="prashasyashok@gmail.com"
series="game of thrones,friends,suits,riverdale"

try:
    cur.execute("insert into users(name,email) values(?,?)",(name,email))
except:
    print("Error. User exists")

series=series.split(",")
for item in series:
    res=cur.execute("SELECT EXISTS(SELECT 1 FROM tv_series WHERE name=(?) LIMIT 1)",(item,))
    for i in res:
        if(i[0]==0):
            cur.execute("insert into tv_series(name) values(?)",(item,))
        else:
            res=cur.execute("select updates from tv_series where name=(?)",(item,))
            for i in res:
                print(i)
res=cur.execute("select * from tv_Series")
for each in res:
    print(each)

con.commit()
con.close()