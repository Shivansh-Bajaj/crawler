import urllib.request
from urllib.parse import urlparse,urljoin
import re
from bs4 import BeautifulSoup
import sqlite3
global start_url

class crawler():
	'''/////////////****************///////////////
	   ////           welcome user            ////
	   ////////////////////////////////////////////
	crawler is class to crawl your website get all the links and store in in data base . After you can search in database
	to crawl your site you need to call crawl function with your site name argument. To search in database call search function with search keyword as argumnet'''
	def __init__(self):
	    global conn
	    global c
	    conn = sqlite3.connect("crawler.db")
	    c = conn.cursor()
	    c.execute('''create table if not exists crawler (url text, title text,visited real)''')
	    conn.commit()
	def crawl(self):
		queue=[start_url]
		while(queue):
			url=queue[0]
			htmlfile=urllib.request.urlopen(url)
			baseurl=urlparse(url).netloc
			print(queue)
			soup=BeautifulSoup(htmlfile.read(),'html.parser')
			for link in soup.findAll('a',href=True):
				if "www" not in link['href']:
					try:
						new_url=urljoin(url,link['href'])
					except:
						print("new_url problem")
					queue.append(new_url)
					p=new_url
					t=link.text
					print(p,t)
					c.execute('''INSERT INTO crawler VALUES (?,?,"0");''',(p,t))
					conn.commit()
				elif baseurl in link['href']:
					queue.append(link['href'])
					p=link['href']
					t=link.text
					#print(p, t)
					c.execute('''INSERT OR REPLACE INTO crawler (url,title,visited)  VALUES (?,?,"0");''',(p,t))
					conn.commit()
			while url in queue:
				queue.remove(url)

	def search(self,text):
		string='%'+text+'%'
		c.execute("SELECT * FROM crawler where title LIKE ('%' || ? || '%')",(string,))
		row=c.fetchall()
		print(row)
		return row
