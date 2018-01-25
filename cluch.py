#! /usr/bin/python3
import threading
import requests
from bs4 import BeautifulSoup as Bs
import re
import pymysql as sql
import time

conn=sql.Connect('localhost','root','')
cur=conn.cursor()
try:
    cur.execute('create database clutch_co')
except Exception as e:
    print(e)

cur.execute('use clutch_co')


class query_exe(threading.Thread):
    def __init__(self,company_id,file_u,company_name,company_contact,company_website,company_location_city,company_location_region,company_employee,company_rating,company_review_count):
        super(query_exe,self).__init__()
        self.company_id=company_id
        self.file_u=file_u
        self.company_name=company_name
        self.company_contact=company_contact
        self.company_website=company_website
        self.company_location_city=company_location_city
        self.company_location_region=company_location_region
        self.company_employee=company_employee
        self.company_rating=company_rating
        self.company_review_count=company_review_count
    def run(self):
        query='insert into clutch_db values("'+self.company_id+'","'+self.file_u+'","'+self.company_name+'","'+self.company_contact+'","'+self.company_website+'","'+self.company_location_city+'","'+self.company_location_region+'","'+self.company_employee+'","'+self.company_rating+'","'+self.company_review_count+'")'
            

        try:    
            cur.execute(query)
            
            
            print('inserted company'+ company_name)
        except Exception as a:
            
            print('query not inserted cause :',a)
        try:
            conn.commit()
        except Exception as r:
            print('fsdfs',r)   



class fetchdata(threading.Thread):
    def __init__(self,num_of_row, new_url,file_u,i):
        super(fetchdata, self).__init__()
        self.i=i
        self.new_url=new_url
        self.file_u=file_u
        self.num_of_row=num_of_row
    def run(self): 
    
        new_url1=self.new_url+'?page='+str(self.i)
        
        print('connecting...............for page '+str(self.i)+ 'of' +str(self.num_of_row))
        
        lunk=self.file_u+'_page'+str(self.i)+'.text'
        try:
            fp=open('cat_page/'+lunk,'r')
            
            page_data=fp.read()
            fp.close()
            if(self.num_of_row==self.i+1):
                fd=open('compelate.text','a')
                fd.write(new_url)
                fd.close()
            
        except Exception as e:
            while True:
                print(new_url1)
                try:    
                    page_data=requests.get(new_url1,timeout=10)
                    if(page_data.status_code==200):
                        
                        fp=open('cat_page/'+lunk,'w+')
                        fp.write(page_data.text)
                        page_data=page_data.text
                        fp.close()
                        
                except Exception as e1:
                    print('trying again after some time due to ',e1)        
                    time.sleep(2)

            
        
        page_1_soup=Bs(page_data,'html.parser')
        

        page_all_lis=page_1_soup.find_all('li',class_='provider-row')

        
        #all seperate 
        count=0
        for lis in page_all_lis:
            li_data=lis.find('div',class_='row')
            try:
                company_location_country=li_data.find('span',class_='country-name').text
            except Exception as e:
                print('company_region not fount ')
                company_location_country=''
            print('company_cccc ',company_location_country)
            try:
                company_id=li_data['data-clutch-nid']
            except Exception as e:
                print('company_id not fount ')
                company_id=''
            query1='update clutch_db set company_location_country="'+company_location_country+'" where company_id="'+company_id+'" '
            try:
                cur.execute(query1)
                conn.commit()
            except Exception as p:
                print('update ',p)
            # try:
            #     company_location_region=li_data.find('span',class_='region').text
            # except Exception as e:
            #     print('company_region not fount ')
            #     company_location_region=''
            # #print('region= '+company_location_region)
            


            # try:
            #     company_id=li_data['data-clutch-nid']
            # except Exception as e:
            #     print('company_id not fount ')
            #     company_id=''
            # #print ('company_id='+company_id)
            # try:
            #     company_website=li_data.find('li',class_='website-link website-link-a').a['href']
            # except Exception as e:
            #     print('company_website not fount for  '+company_name)
            #     company_website=''

            # try:
            #     company_name=li_data.find('h3',class_='company-name').text.strip()
            # except Exception as e:
            #     ind=re.match(r'http://(www)?(.*)\.',company_website).group()
            #     company_name=ind.replace(r'http://','').replace('www.','').replace('.','')
            # if(company_name==''):
            #     ind=re.match(r'http://(www)?(.*)\.',company_website).group()
            #     company_name=ind.replace(r'http://','').replace('www.','').replace('.','')
                
            
            # #print('company_name = '+company_name)

            # try:
            #     company_rating=li_data.find('span',class_='rating').text
                
            # except Exception as e:
            #     print('company_rating not fount ')
            #     company_rating=''
            
            # #print('company_rating='+company_rating)
            
            # try:
            #     company_review_count=li_data.find('span',class_='reviews-count').a.text.split(' ')[0]
            
            # except Exception as e:
            #     print('company_review not fount ')
            #     company_review_count=''
            
            # #print('company_review='+company_review_count)
            
            
            # try:
            #     company_employee=li_data.find('span',class_='employees').text
            # except Exception as e:
            #     print('company_emp not fount ')
            #     company_employee=''
            
            # #print('num_employee= '+company_employee)

            
            
            # try:
            #     company_location_city=li_data.find('span',class_='locality').text[:-1]
            # except Exception as e:
            #     print('company_city not fount ')
            #     company_location_city=''
            
            # #print('company_location_city= '+company_location_city)
            # #print('company_website= '+company_website)
            # try:
            #     company_contact=li_data.find('div',class_='item __color6a').text.strip()
            # except Exception as e:
            #     print('company_contact not fount ')
            #     company_contact=''
            
            # #print('company_contact='+company_contact)
            # tr=query_exe(company_id,file_u,company_name,company_contact,company_website,company_location_city,company_location_region,company_employee,company_rating,company_review_count).start()
            # tr.join()
            
           
        print('Thread Completed')
                

#url='https://clutch.co'

#website_data=requests.get(url)



#website_soup=Bs(website_data.text,'html.parser')

#print(website_soup.prettify())

categories_Url='https://clutch.co/directories'

print('connecting...........for initialising')
try:
    categories_html=requests.get(categories_Url)
except Exception as p:
    print(p)
categories_Soup=Bs(categories_html.text,'html.parser')
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
sql='create table clutch_db(company_id varchar(100),company_category varchar(200),company_name varchar(100),company_contact varchar(100),company_website varchar(200),company_location_city varchar(100),company_location_region varchar(100),company_employee varchar(100),company_rating float(10),company_review_count int(10),PRIMARY KEY(company_id))'
       
try:
    cur.execute(sql)
except Exception as e:
    print(e)

count=0
for head in header_item[:]:
    cat_link=cat_dict[head]
    link=list(cat_dict[head].keys())

    for links in link:
        print('categ = ',count)
        count+=1
        url='https://clutch.co'

        new_url=url+cat_link[links]
        # try:
        #     fd=open('compelate.text','r+')
        #     data3=fd.read()
        #     fd.close()
        #     if(new_url in data3):
        #         print('stopppppppppp........')
        #         break
        # except Exception as t:
        #     print(t)
        print('connecting...............catag '+new_url)
        file_u=cat_link[links].replace('/','_')
        print('file_u........',file_u)
        if(file_u[0].isalpha()):
            pass
        else:
            file_u=file_u[1:]
        if(file_u[-1].isalpha()):
            pass
        else:
            file_u=file_u[:-1]
        new_content=''
        try:

            fp=open('catag/'+file_u+'.text','r')
            new_content=fp.read()
            print()
            print('file eXiSt...........')
            print()
            fp.close()
           
        except Exception as e:
            print('trying..... ',new_url)
            while True:
                try:
                    new_content=requests.get(new_url)
                    new_content=new_content.text
                    fp=open('catag/'+file_u+'.text','w+')
                    fp.write(new_content)
                    fp.close()
                    break
                except Exception as r:
                    print(r)
            

                
                
                    

        page_soup=Bs(new_content,'html.parser')
        try:
            num_of_row=page_soup.find('li',class_='pager-current').text
            num_of_row=int(num_of_row.split(' ')[-1])
        except Exception as a:
            print(a)
            
        print('FOR LOOP START.........for ',file_u)
        
        for i in range(num_of_row):
            try:
                print('new thread start')
                ar=fetchdata(num_of_row,new_url,file_u,i)
                ar.start()
                if(ar.join()):
                    continue
            except Exception as e2:
                print('thread error ',e2)


    
                   
        
print()
print('done')
flag=('You Want To Commit [Y/N]')
if(flag.lower()=='y'):
    
    conn.commit()
    conn.close()
else:
    conn.close()
