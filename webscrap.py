#! /usr/bin/python3
import requests
import pymysql as sql
import re
from bs4 import BeautifulSoup as Bs
url = 'https://www.goodfirms.co'
print(url)
conn=sql.Connect('localhost','root','')
cur=conn.cursor()

data = requests.get(url)
soup = Bs(data.text,'html.parser')
divs = soup.find_all('div',class_='frontbannerdivb')
target = {}
mytarget = ['Mobile App Development','Software Development','Web Development','Blockchain Technology','E-commerce Development','Digital Marketing']

subcategores={'Mobile App Development':['iphone','Android','ipad','Hybrid'],'Software Development':['PHP','Ajax','Node.js','Angularjs','Python'],'Web Development':['Wordpress'],'Blockchain Technology':['Smart Contract','Private Blockchain'],'E-commerce Development':['Shopify','Woocommerce'],'Digital Marketing':['SEO','Content Marketing','SMM','Advertising & PPC','App Marketing','Email Marketing','Local Marketing','Branding']}
subcategores1={}

for data in divs:
    if data.a.text in mytarget:
        target[data.a.text] = data.a['href']
subcats=soup.find_all('ul',class_='left-submenu')
allli=subcats[0].find_all('li',class_='vcategory-menu')

for cont in allli:
    
    if(cont.a.text in mytarget):
        title=cont.a.text
        subs=cont.div.div.div.ul
        subs=subs.find_all('li')
        
        for i in range(1,len(subs)):
            subcategores1[subs[i].a.text]=subs[i].a['href']
            
print(len(subcategores1))
        # for i in range(1,len(subs)):
        #     if(subs[i].span.text in subcategores[subs[0].span.text]):
        #         subcategores1[subs[0].span.text].append(subs[i].span.text)
  
#new loop
fetchdata=target[mytarget[3]]
database_name=mytarget[3].split(' ')
database_name='_'.join(database_name)
try:
    database=cur.execute('create database '+database_name)
except Exception as e:
    print(e)

cur.execute('use '+database_name)
tablename=subcategores[mytarget[3]][0]
tablename=tablename.split(' ')
tablename='_'.join(tablename)
print('table name :'+tablename)
try:
    var='create table '+tablename+'(Company_Name varchar(100),Company_Website varchar(100),Company_Location varchar(100),Company_Employee varchar(100),Company_Founded_in varchar(100))'
    print(var)
    cur.execute(var)
except Exception as e:
    print(e)

fetchdata=url+subcategores1[subcategores[mytarget[4]][0]]

print('Link is :-'+fetchdata)
page=requests.get(fetchdata)

pagesoup=Bs(page.text,'html.parser')
#print(pagesoup.prettify())
flag=0
try:
    number_of_page=pagesoup.find_all('a',href=True,title='Last page')[0]['href']
    indexes= number_of_page.index('page')
    print(indexes)
    number_of_page=number_of_page[indexes+5:]
    print(number_of_page+' pages found in this Catagory')
    flag=1
except Exception as e:
    print(e)
if(!flag)
    
#new loop for all pages
fetchdata+='/page:'+str(1)
company_data=requests.get(fetchdata)
company_pagesoup=Bs(company_data.text,'html.parser')


