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

#url='https://clutch.co'

#website_data=requests.get(url)



#website_soup=Bs(website_data.text,'html.parser')

#print(website_soup.prettify())

# categories_Url='https://clutch.co/directories'
# categories_html=requests.get(categories_Url)
fp=open('file.text','r')
ht=fp.read()
fp.close()

categories_Soup=Bs(ht,'html.parser')
#print(categories_Soup.prettify())
categories_h2=categories_Soup.find_all('h2')
header_item=[]
headers={}
for h2 in categories_h2:
    if(h2.a):
        headers[h2.a.text]=h2.a['href']
        header_item.append(h2.a.text)
    else:
        pass

cat_dict={}
categories_div=categories_Soup.find_all('div',class_='field-items')

headers_keys=list(headers.keys())

for i in range(len(headers)):
    categories_div_1=categories_div[0].div
    
    

    categories_div_row=categories_div_1.find_all('div',class_="row",recursive=False)

    main_cat={}
    temp_div=categories_div_row[i].find_all('div',class_='col-md-3 col-sm-6 col-xs-12')
    temp_ul=temp_div[0].find_all('ul',recursive=False)
    print(i,' ',len(temp_ul))
    if(len(temp_ul)):
        
        li=temp_ul[0].find_all('li',recursive=False)
        
        for lia in li:
            if(lia.a):
                main_cat[lia.a.text]=lia.a['href']
    # print(header_item[i])
    # print(main_cat)
    cat_dict[header_item[i]]=main_cat

for i in header_item:
    print(i)
    print(cat_dict[i])
    print()
    
