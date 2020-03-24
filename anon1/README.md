
# Overview

The goal of this project is to scrape and tabulate the job titles for several companies from their careers pages. For each company, I filter to the jobs located in the US with the word "engineering" in the job title. Then I count the number of jobs available for each city. This information is useful for a research project I'm working on about the effect of tech companies on local neighborhoods. 

# Contents
* README.md - this file
* 01_scrape.py - the Python script with my code
* 01_scrape.ipynb - Same as 01_scrape.py, except in a Python notebook. 
* output.txt - Output text produced by 01_scrape.py if you run it in a terminal
* output/ - folder containing all csv files output by 01_scrape.py
* final_project - video, shared via Google Drive: <https://drive.google.com/open?id=1gM_YJ2mk5TqmskcLa5K9OgAuDOd5rJHz>
* requirements.txt - packages installed

# Technical Overview

## Code Design

There is a parent class called `Company`, and there is one child class for each of the companies that I want to scrape: `Microsoft`, `Jpmorgan`, `Google`, and `HomeDepot`. The child classes inherit the methods in `Company`, add their own methods, and overwrite some of the methods in the parent class.

## Modules

The only module is 01_scrape.py.

The `main` function initializes the class for a specific company and calls the `query` method for each of the 4 child classes. In all 4 child classes, `query` is inherited from the parent.

The parent class, `Company`, has these methods: `get_url`, `query`, `scrape_data`, `clean_data`, and `tabulate_data`. `get_url` takes in an URL, sends a request, parses the response into an html object using beautiful soup, and returns the soup object. `query` is contains the 3 main steps executed for each company that I need to look up. The 3 functions it calls are `scrape_data`, `clean_data`, and `tabulate_data`. In the parent class, these 3 functions are empty - they will be specified in the child class. 

The first child of the parent class is `Microsoft`. It inherits `query` from the parent class `Company`. `scrape_data` scrapes the data for each page by calling `get_dataframe`, which puts a json object of all of the jobs for each page into a dataframe and returns it. To know how many pages to scrape, `scrape_data` calls `get_num_jobs`. `scrape_data` concatenates all the dataframes for each page into a single dataframe and outputs the csv file `microsoft.csv`. Next, `clean_data` reads in `microsoft.csv` and filters to only engineering jobs in the US, and outputs the file `microsoft_US_engineer.csv`. Finally, `tabulate_data` reads in `microsoft_US_engineer.csv`, tabulates the number of job titles for each location, and outputs `microsoft_tabbed.csv`. 

The other child classes are `Jpmorgan`, `Google`, and `HomeDepot`. They work very similarly to `Microsoft` with a few exceptions detailed below: 

* `Microsoft`: 
    - Has `clean_soup` and `get_json` methods, which are helper functions used in `get_dataframe` to clean the soup string and return the json object.
* `Jpmorgan`: 
    - Has `get_tags1` and `get_tags2`, which are helper functions used by `get_dataframe` to extract and clean the html tags.
    - Has `get_num_jobs` instead of `get_num_pages` method because the url format uses number of jobs.
* `Google`:
    - `get_url` overwrites the method from the parent class because the object returned from requests is a json object that we can directly read in without converting to a beautiful soup object. 
    - Has `get_num_jobs` instead of `get_num_pages` method because the url format uses number of jobs.
* `HomeDepot`:
    - `get_url` overwrites the method from the parent class because we need to use webdriver to get the html code. 
    - `get_list_text` is a method used by `get_dataframe` that uses a list comprehension(!) to extract the text portion of the html code from each element in the list.

## Requirements
I recommend running it from Jupyter Notebook instead of the Terminal.

# Installation/Execution Instructions

1. Make sure all packages needed are installed (note that the `webdriver` package is difficult to install, and it's possible that my code will only run on Parth's computer because he had to do some weird configuration on my computer to get `webdriver` to work properly). In case you can't install webdriver successfully, I've included my Terminal output in a file called output.txt.
2. Create a folder in the current directory called "output." 
3. Run 01_scrape.py. See Known Bugs for details if the code breaks.

# Credits/Acknowledgements
Thanks to Parth for helping me get webdriver to work. I used some code from <https://medium.com/the-andela-way/introduction-to-web-scraping-using-selenium-7ec377a8cf72> to implement waiting for the page to load in webdriver.

# Known Bugs
* If it's breaking in the HomeDepot class, then try extending the waiting time beyond 5 seconds to 10 seconds.  
* Sometimes you have to try running 01_scrape.py a few times before it works. It randomly breaks in different parts for no apparent reason, but chances are that if you run it 5 times, it will work at least once. Note that this random breakage never happens when the code is run in a Jupyter Notebook. It's only when running the Python script that the problem occurs. 