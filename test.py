import re
val='http://rjk.com/jbjbas/sbxkhmsxa/'
ind=re.match(r'http://(www)?(.*)\.',val)
r=ind.group().replace(r'http://','').replace('www.','').replace('.','')
print(r)