import requests
from bs4 import BeautifulSoup
import time
import json
def process(**kwargs):
	cache={}
	date=kwargs['date']
	month=kwargs['month']
	headline=""
	with open("floridamanDict.json") as f:
		cache = json.load(f)
	searchDate = str(month)+" "+str(date)
	if searchDate in cache.keys():
		return "On "+ searchDate +": {}".format(cache[searchDate])
	else:
		query = "florida man" + searchDate + "news - ifunny" 
		for j in search(query, tld="com", num=1, stop=1, pause=2):
			try:
				page=requests.get(j, timeout=5, headers={'User-Agent':'Headline Scraper Script by @jcorbin'})
			except requests.exceptions.RequestException:
				floridaString = "No result found!"
			if floridaString!= "No result found!":
				coverpage=page.content
				soup1 = BeautifulSoup(coverpage, 'html5lib')
				if soup1.head.find('title') is not None:
					headline = soup1.head.find('title').get_text()
				else:
					headline = str(current)
				return headline
			else:
				return "Sorry, no result found!"
			
