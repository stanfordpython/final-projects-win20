The Florida Man by Corbin Schmeil and Dylan Ly

	The Florida Man website will be one in which the user can enter their birthdate and find out the headline of what the Florida Man did on their birthday. 


The general overview of the program:

	We created a cache dictonary of all possible birthdays to the corresponding article title about the Florida Man. 

	date.py: An initial problem we came across was trying to iterate over the days of a year and find the corresponding months. To solve this, we began by importing a calendar library to iterate over the days of a year. Date.py iterates over the days of a specific year (taking into account leap years). 

	floridaman_urls.py: Once we were able to convert the days and months of the year to number values we then conducted a google search with the format: "florida man" + the search date + "news -ifunny". Using web requests, we searched using Google. We took out "ifunny" from the search results because that website was specifically always causing errors. We chose the first article out of the ones presented and saved this url. We amassed a list of url's that were links to news articles about the Florida Man's crimes on all days of the year. 

	floridaman.py: Once we ammassed the list of appropriate URL's, we used the Beautiful Soup library to web scrape the articles for the information we wanted: article titles. In the thread of the pages, we looked for the "title" notation and retrieved the text connected to the title. The corresponding line of code was along the lines of: 
		- soup.head.find('title').get_text()
	Once we were able to isolate the article heading, we added the text to the dictionary that linked birthday's to headings. We ran into problems since every website we searched for was different. The 'title' label would occasionaly be different between different websites. By refining our search, we managed to filter out buggy websites. 

	floridamanconsole.py: On the console, we prompt the user to enter a date see what the Florida Man did on that day. According to what month they enter, we prompt them to enter a day within a certain range. For example, the user will be promted to enter a date between 1-30 or 1-31 based off of the month they choose. 
    We ultimately re-implemented this into the 'process' module as is described in the website form template that was on piazza, in order to get it to work with flask. So everything in the 'floridamanapp' folder is just stuff from the 'floridamanbirthday' folder either reimplemented or supplemented to do the same thing but display it on a flask webpage.

	We will implement the program via Heroku in order to get an active website that users can interact with. We configured our app based on the template from Piazza in flask and then pushed the program to Heroku to get an active website. The website will pull information from the dictionary we created before hand so the user will not need to download any external program. The dictionary will be in a file that the website will use to return informaiton to the user


Execution instructions:
	
	The code we will be submitting contains everything different aspects of the code also produced. If you wanted to do eveything from the ground up, the order would be: run florudaman_urls.py, then run floridaman.py, then if you wanted to run in terminal: run floridamanconsole.py. Alternatively, if you wanted to go the heroku route, once you had run the first two you would move the file 'floridamanDict.json', which is created by floridaman.py, into the folder with the 'floridamanapp' stuff, create a Procfile that says 'web: gunicorn app:app', create a requirements.txt, and then push to heroku. We already did all that though, so you can also just click the link. There are some weird instances which make the server crash, which if we had more time we would fix, but as of now it's not perfect.
    We will have a website link with everything you need to know to enter your birthdate. There will be options to enter your birth month and day and the website will then tell you what the Florida Man did on that day!

	Here is the link! Enjoy!: floridamanapp.herokuapp.com


Publishing permissions:

	We wouldn't mind if you all shared the link to the website on the CS 41 website! It is a program that hopefully will make some people smile. 











