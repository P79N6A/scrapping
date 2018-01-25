#! /usr/bin/python3
import requests
import pymysql as sql
import re
import threading
import time
import os
from bs4 import BeautifulSoup as Bs
url = 'https://www.goodfirms.co'
print(url)
conn=sql.Connect('localhost','root','')
cur=conn.cursor()
cur.execute('use goodfirms_db')
data = requests.get(url)
soup = Bs(data.text,'html.parser')
divs = soup.find_all('div',class_='frontbannerdivb')
target = {}
mytarget = ['Mobile App Development','Software Development','Web Development','Blockchain Technology','E-commerce Development','Digital Marketing']

subcategores={'Mobile App Development':['iphone','Android','ipad','Hybrid'],'Software Development':['PHP','Ajax','Node.js','Angularjs','Python'],'Web Development':['Wordpress'],'Blockchain Technology':['Smart Contract','Private Blockchain'],'E-commerce Development':['Shopify','Woocommerce'],'Digital Marketing':['SEO','Content Marketing','SMM','Advertising & PPC','App Marketing','Email Marketing','Local Marketing','Branding']}
subcategores1={}

class query(threading.Thread):
    def __init__(self,name,website,location,employee,founded_in):
        self.name=name
        self.website=website
        self.location=location
        self.employee=employee
        self.founded_in=founded_in
    def run(self):
        qr='insert into goodfirms_db values("'+self.name+'","'+self.website+'","'+self.location+'","'+
        self.employee=employee
        self.founded_in=founded_in)'
        cur.execute(')

class pagedata(threading.Thread):
    def __init__(self,site_url,number_of_pages,dir,subdir):
        super(pagedata,self).__init__()
        self.site_url=site_url
        self.number_of_pages=int(number_of_pages)
        self.dir=dir
        self.subdir=subdir
    def run(self):
        soupdata=''
        print('loop start')
        for i in range(self.number_of_pages):
                try:
                    fp=open(self.dir+'/'+self.subdir+'/page:'+str(i)+'.text','r')
                    soupdata=fp.read()
                    fp.close()
                except Exception as o:
                    print(o)
                    while True:
                        try:
                            print('connecting to ',self.site_url+'/page:'+str(i))
                            html_data=requests.get(self.site_url+'/page:'+str(i),timeout=10)
                            soupdata=html_data.text
                            fp=open(self.dir+'/'+self.subdir+'/page:'+str(i)+'.text','w+')
                            fp.write(html_data.text)
                            fp.close()
                            break
                        except Exception as t:
                            print(t)
                            pass
                page_soup1=Bs(soupdata,'html.parser')
                divs=page_soup1.find_all('div',class_='whitebg border radious4 margin-bottom col-md-12 no-padding greenborder overflow commoncompanydetail')
                for div in divs:
                    try:
                        company_name=div.find('div',class_='company-info-title').h3.a.text
                    except Exception as e:
                        print(e)
                    print('name : '+company_name)

                    try:
                        company_website=div.find('a',class_='visit-website block default-blue-btn c_visit_website')['href']
                    except Exception as e:
                        print(e)
                    print('website : ' +company_website)

                    spans=div.find('div',class_='clear overflow border-top border-bottom compny-service-review').find_all('div',recursive=False)
                    print(len(spans))
                    
                    
                    try:
                        company_location=spans[1].find('div',class_='blackc font14 lhnormal').text
                    except Exception as e:
                        print(e)
                    print('Location : '+company_location)

                    try:
                        company_employee=spans[2].find('div',class_='blackc font14 lhnormal').text
                    except Exception as e:
                        print(e)
                    print('Employee : '+company_employee)  

                    try:
                        company_Founded_in=spans[3].find('div',class_='blackc font14 lhnormal').text
                    except Exception as e:
                        print(e)
                    print('found : '+company_Founded_in)
 
                    a=input('hello:')        

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
os.system('mkdir '+database_name)


tablename=subcategores[mytarget[3]][0]
tablename=tablename.split(' ')
tablename='_'.join(tablename)
print('table name :'+tablename)

os.system('mkdir '+database_name+'/'+tablename)
try:
    var='create table goodfirms_data(Company_Name varchar(100),Company_Website varchar(100),Company_Location varchar(100),Company_Employee varchar(100),Company_Founded_in varchar(100))'
    
    cur.execute(var)
except Exception as e:
    print(e)

fetchdata=url+subcategores1[subcategores[mytarget[4]][0]]

print('Link is :-'+fetchdata)
page=requests.get(fetchdata)
print(fetchdata)
pagesoup=Bs(page.text,'html.parser')
#print(pagesoup.prettify())
flag=0
try:
    number_of_page=pagesoup.find_all('a',href=True,title='Last page')[0]['href']
    indexes= number_of_page.index('page')
    number_of_page=number_of_page[indexes+5:]
    print(number_of_page+' pages found in this Catagory')
    flag=1
except Exception as e:
    print(e)
if(flag!=0):
    #new loop for all pages
    
    pagedata(fetchdata,number_of_page,database_name,tablename).start()
    
    


