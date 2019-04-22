import sys
from requests import get
import datetime
from bs4 import BeautifulSoup as soup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from string import Template
import sqlite3 as sql


def switcher(argument):
	switch={
	"Jan" : 1,
	"Feb" : 2,
	"Mar" : 3,
	"Apr" : 4,
	"May" : 5,
	"Jun" : 6,
	"Jul" : 7,
	"Aug" : 8,
	"Sep" : 9,
	"Oct" : 10,
	"Nov" : 11,
	"Dec" : 12
	}
	return switch.get(argument)

def get_q(series):
	name=""
	for word in series.split():
		name=name+word+"+"
	name=name[:len(name)-1]
	return name

def get_date(a):
	a=a.split()
	if len(a)==2:
		return a
	a[1]=a[1][:3]
	a[1]=switcher(a[1])
	return a



def read_template():
    with open('message.txt', 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def send(to,message):
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.ehlo()
	s.starttls()
	s.login("prashasyashok@gmail.com","inteli007")

	msg=MIMEMultipart()
	msg['From']='prashasyashok@gmail.com'
	msg['To']=to
	msg['Subject']="TV Show Notifier | Updates on your favourite TV Series"
	msg.attach(MIMEText(message, 'plain'))
	s.send_message(msg)
	del msg
	s.quit()









def imdb_data(series):


	query="https://www.imdb.com/find?ref_=nv_sr_fn&q={}&s=all".format(get_q(series))
	response=get(query)	
	html=soup(response.content,'html.parser')
	
	tag=html.find_all("div",class_="findSection")
	url=""
	for section in tag:
		t=section.find("h3","findSectionHeader")
		if(t.text=="Titles"):
			table=section.find("table",class_="findList")
			table=table.find_all("td",class_="result_text")
			for td in table:
				if("TV Series" in td.text and not td.find("small") and td.a.text.lower()==series.lower()):
					url=td.find("a")['href']
					url="https://www.imdb.com{}".format(url)
					break	


	if(url==""):
		return "Could not search for the TV Series. Exiting..."
	response=get(url)
	html=soup(response.content,'html.parser')
	# f=open("website_data.txt",'r')
	# html=soup(f,'html.parser')
	# f.close()

	tag = html.find('div',class_="seasons-and-year-nav")
	seasons="https://www.imdb.com/{}".format(tag.find('a')['href'])
	response=get(seasons)
	html=soup(response.content,'html.parser')
	next=""
	flag=0
	for date in html.find_all('div',class_='airdate'):
		if len(date.text)==1:
			flag=2
			continue
		if len(date.text)==22 or len(date.text)==27:
			next="The next season begins in {}".format((date.text).strip())
			flag=1
			break
		print(date.text.strip())
		d=get_date(date.text.strip())
		print (d)
		now=datetime.datetime.now()
		if int(d[2])>now.year:
			next="The next episode airs on {}".format(date.text.strip())
			flag=1
			break
		if int(d[2])==now.year:
			if int(d[1])>=now.month:
				if(int(d[0])>=now.day):
					next="The next episode airs on {}".format(date.text.strip())
					flag=1
					break
	if flag==0:
		next="The show has finished streaming all its episodes."
	if(flag==2):
		next="The next showing date is not available"

	return next




def main(user,email,series):
	# user=input("Name: ")
	# email=input("Email: ")
	# series=input("Series: ")
	series=series.split(',')
	print(series)
	msg=""
	m=''

	con=sql.connect("user_data.db")
	cur=con.cursor()


	try:
		cur.execute("insert into users(uname,email) values(?,?)",(user,email))
	except:
		print("Error. User exists")
		return

	for item in series:
		res=cur.execute("SELECT EXISTS(SELECT 1 FROM tv_series WHERE name=(?) LIMIT 1)",(item,))
		for i in res:
			if(i[0]==0):

				m+="TV Series: "+item +"\n" +"Status: "+imdb_data(item)+"\n\n"
				print(m)
				cur.execute("insert into tv_series(name,updates) values(?,?)",(item,m))
			else:
				res=cur.execute("select updates from tv_series where name=(?)",(item,))
				for i in res:
					m+=i[0]
					print(i)

	con.commit()
	con.close()





	msg+=m


	message_template = read_template()
	message = message_template.substitute(person=user,body=msg)
	send(email,message)
	print(message)
	return(msg)


if __name__=='__main__':
	main()
