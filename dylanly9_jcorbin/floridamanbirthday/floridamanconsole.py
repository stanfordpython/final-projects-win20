import json
import calendar
import requests
import date
from bs4 import BeautifulSoup
import time
cache={}
with open("floridamanDict.json") as f:
	cache = json.load(f)
print ("Welcome to floridamanbirthday. Please enter a date to see what florida man did on this day...")
while True:
	months=['January','February','March','April','May','June','July','August','September','October','November','December']
	monthAnswer=""
	dateAnswer=""
	while (monthAnswer := input("What is the month?(the full name please): ".capitalize())) not in months:
		print("Please enter a month correctly!: ")
	if monthAnswer == 'February':
		while (dateAnswer:= int(input("Enter a day number 1-28: "))) not in range(1,29):
			print("Please enter a date in the given range!: ")
	elif monthAnswer in ['September' , 'April' , 'June' , 'November']:
		while (dateAnswer:= int(input("Enter a day number 1-30: "))) not in range(1,31):
			print("Please enter a date in the given range!")
	elif monthAnswer in ['January' , 'March' , 'May' , 'July' , 'August' , 'October' , 'December']:
		while (dateAnswer:= int(input("Enter a day number 1-31: "))) not in range(1,32):
			print("Please enter a date in the given range!: ")
	searchDate = str(monthAnswer)+" "+str(dateAnswer)
	print (searchDate)
	if searchDate in cache.keys():
		print ("On " + searchDate + ": "+cache[searchDate])
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
				headline=""
				if soup1.head.find('title') is not None:
					headline = soup1.head.find('title').get_text()
				else:
					headline = str(current)
			else:
				print("Sorry, no result found!")
		print (headline)
	again=input("Would you like to try another date? If so, type 'y': ")
	if again != 'y':
		break
print ("Thanks for trying!")