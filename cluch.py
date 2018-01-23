#! /usr/bin/python3

import requests
from bs4 import BeautifulSoup as Bs
import re
import pymysql as sql

conn=sql.Connect('localhost','root','')
cur=conn.cursor()
try:
    cur.execute('create database clutch_co')
except Exception as e:
    print(e)

cur.execute('use clutch_co')

url='https://clutch.co'

website_data=requests.get(url)

website_soup=Bs(website_data.text,'html.parser')

#print(website_soup.prettify())

categories_Url='https://clutch.co/directories'
categories_html=requests.get(categories_Url)
categories_Soup=Bs(categories_html.text,'html.parser')
#print(categories_Soup.prettify())
categories_h2=categories_Soup.find_all('h2')

headers={}
for h2 in categories_h2:
    if(h2.a):
        headers[h2.a.text]=h2.a['href']
        
    else:
        pass
categories_div=categories_Soup.find_all('div',class_='row')
print(len(categories_div))
