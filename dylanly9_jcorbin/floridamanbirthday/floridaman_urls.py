import requests
import date
from bs4 import BeautifulSoup
import time
import json
try: 
    from googlesearch import search
except ImportError:  
    print("No module named 'google' found") 
urls = []

	query = "florida man" + searchDate + " news -ifunny"
	urls = []
	url=""

	for j in search(query, tld="com", num=1, stop=1, pause=2): 
		urls.append(j)
		print(j)
		url = j
print (urls)
with open('urls.txt', 'w') as f:
    for item in urls:
        f.write("%s\n" % item)
