#!/usr/bin/env python
# coding: utf-8

import ast
from bs4 import BeautifulSoup
import collections
import csv
import json
import math
import numpy as np
import os
import pandas as pd
import re
import requests
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException


OUTPUT_DIR = 'output/'


class Company:

    def get_url(self, url):
        """For a given job posting URL, returns the beautiful soup object.
        Arguments:
        url -- URL to query
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def query(self):
        self.scrape_data()
        self.clean_data()
        self.tabulate_data()

    def scrape_data(self):
        pass

    def clean_data(self):
        pass

    def tabulate_data(self):
        pass


class Microsoft(Company):

    def clean_soup(self, soup):
        """Takes beautiful soup object, removes excess strings, and returns json object.
        Arguments:
        soup -- beautiful soup object
        """
        soup_str = soup.script.string
        start_str = ' /*<!--*/ var phApp = phApp || {"widgetApiEndpoint":"https://careers.microsoft.com/professionals/widgets","country":"us","deviceType":"desktop","locale":"en_us","absUrl":true,"refNum":"MICRUS","cdnUrl":"https://prodcmscdn.azureedge.net/careerconnectresources/p","baseUrl":"https://careers.microsoft.com/professionals/us/en/","baseDomain":"https://careers.microsoft.com/professionals","phenomTrackURL":"careers.microsoft.com/professionals/us/en/phenomtrack.min.js","pageName":"search-results","siteType":"professionals","rootDomain":"https://careers.microsoft.com","pageId":"page906"}; phApp.ddo = '
        sep_str = '; phApp.sessionParams = '
        soup_str = soup_str.replace(start_str,'',1)
        soup_str = soup_str.split(sep_str, 1)[0] # remove everything after sep_str
        json_file = json.loads(soup_str) # convert to json
        return json_file

    def get_json(self, url):
        """Takes url and returns json object.
        Arguments:
        url -- url string
        """
        soup = self.get_url(url)
        json = self.clean_soup(soup)
        return json

    def get_dataframe(self, num):
        """Takes list of jobs for a given page number and inserts it into a dataframe. Returns a dataframe.
        Arguments:
        num -- page number
        """
        num_str = str(num)
        url = 'https://careers.microsoft.com/professionals/us/en/search-results?keywords=engineer&from=' + num_str + '&s=1'
        json_file = self.get_json(url)
        jobs = json_file['eagerLoadRefineSearch']['data']['jobs'] # extract jobs
        df = pd.DataFrame(jobs) # put in dataframe
        return df

    def get_num_jobs(self):
        """Computes and returns the total number of jobs found."""
        url = 'https://careers.microsoft.com/professionals/us/en/search-results?keywords=engineer'
        json_file = self.get_json(url)
        num_jobs = json_file['eagerLoadRefineSearch']['totalHits'] # extract total number of jobs
        return num_jobs

    def scrape_data(self):
        """Scrapes data and outputs to csv file. """
        print("Scraping Microsoft...")
        microsoft = self.get_dataframe(0)
        num_jobs = self.get_num_jobs() # get total number of results
        for i in range(50,num_jobs,50):
            microsoft = pd.concat([self.get_dataframe(i), microsoft])
        microsoft.to_csv(OUTPUT_DIR+'microsoft.csv')
        print("Done scraping.")

    def clean_data(self):
        """Reads in csv, cleans data, and outputs to csv file."""
        print("Extracting US Engineering jobs...")
        microsoft = pd.read_csv(OUTPUT_DIR+'microsoft.csv')
        microsoft = microsoft[microsoft['title'].str.lower().str.contains('engineer')] # get only titles with "engineer"
        microsoft = microsoft[microsoft['country']=='United States'] # get only jobs in US
        microsoft.to_csv(OUTPUT_DIR+'microsoft_US_engineer.csv')

    def tabulate_data(self):
        """Tabulates data by reading in csv file and outputting tabbed csv file."""
        print("Tabulating number of open job titles by city for Microsoft...")
        df_microsoft = pd.read_csv(OUTPUT_DIR+'microsoft_US_engineer.csv')
        df_microsoft = df_microsoft.reset_index()
        df_microsoft = df_microsoft.drop(['index'], axis=1)
        location_lst = []
        for i in range(len(df_microsoft)):
            loc_lst = ast.literal_eval(df_microsoft.multi_location_array[i])
            for loc in loc_lst:
                location_lst.append(loc['location'])
        locs = df_microsoft['location'].tolist()
        all_locations = pd.Series(location_lst + locs)
        loc_tabbed = all_locations.astype('str').value_counts()
        df_microsoft_tabbed = pd.DataFrame(loc_tabbed)
        df_microsoft_tabbed.rename(columns={0: "num_job_openings"}, inplace = True)
        df_microsoft_tabbed.to_csv(OUTPUT_DIR+'microsoft_tabbed.csv')
        print("Here are the number of open job titles by city:")
        print(df_microsoft_tabbed)


class Jpmorgan(Company):

    def get_tags1(self, html_class, soup):
        """Extracts the html_class from the soup object and does minor cleaning. Cleans version 1.
        Arguments:
        html_class -- class tag from html
        soup -- beautiful soup object
        """
        dest_list = soup.find_all(class_=html_class) 
        dest = []
        for item in dest_list:
            dest.append(item.get_text().replace('\n',''))
        return dest

    def get_tags2(self, html_class, soup):
        """Extracts the html_class from the soup object and does minor cleaning. Cleans version 2.
        Arguments:
        html_class -- class tag from html
        soup -- beautiful soup object
        """
        dest_list = soup.find_all(class_=html_class)
        dest = []
        for item in dest_list[1:]:
            dest.append(item.get_text().replace('\r\n','').replace('                    ',''))
        return dest
    
    def get_dataframe(self, num):
        """Takes list of jobs for a given page number and inserts it into a dataframe. Returns a dataframe.
        Arguments:
        num -- page number
        """
        pagenum = str(num)
        url = 'https://jobs.jpmorganchase.com/ListJobs/ByKeyword/engineer/Page-' + pagenum
        soup = self.get_url(url)
        df_jpmorgan = pd.DataFrame()
        df_jpmorgan['job_title'] = self.get_tags1(html_class='coloriginaljobtitle', soup=soup)
        df_jpmorgan['jobid'] = self.get_tags1(html_class='coldisplayjobid', soup=soup)[1:]
        df_jpmorgan['location_city'] = self.get_tags2(html_class='colcity', soup=soup)
        df_jpmorgan['location_state'] = self.get_tags2(html_class='colstate', soup=soup)
        df_jpmorgan['location_country'] = self.get_tags2(html_class='colcountry', soup=soup)
        df_jpmorgan['date_posted'] = self.get_tags2(html_class='colpostedon', soup=soup)
        return df_jpmorgan

    def get_num_pages(self):
        url = 'https://jobs.jpmorganchase.com/ListJobs/ByKeyword/engineer/'
        soup = self.get_url(url)
        total_results = soup.find(class_='pager_counts')
        num_results = int(total_results.contents[0].split(' of ')[1])
        total_num_pages = math.ceil(num_results/30)
        return total_num_pages

    def scrape_data(self):
        """Scrapes data and outputs to csv file. Returns dataframe. """
        print("Scraping JPMorgan...")
        jpmorgan = self.get_dataframe(1)
        num_pages = self.get_num_pages() # get total number of results
        for i in range(2,num_pages+1):
            jpmorgan = pd.concat([self.get_dataframe(i), jpmorgan])
        jpmorgan.to_csv(OUTPUT_DIR+'jpmorgan.csv')
        print("Done scraping.")
        return jpmorgan

    def clean_data(self):
        """Reads in csv, cleans data, and outputs to csv file."""
        print("Extracting JP Morgan US Engineering jobs...")
        df_jpmorgan = pd.read_csv(OUTPUT_DIR+'jpmorgan.csv')
        df_jpmorgan = df_jpmorgan[df_jpmorgan['job_title'].str.lower().str.contains('engineer')] # get only titles with "engineer"
        df_jpmorgan = df_jpmorgan[df_jpmorgan['location_country'] == 'US'] # get only US
        df_jpmorgan = df_jpmorgan.reset_index()
        df_jpmorgan = df_jpmorgan.drop(['index', 'Unnamed: 0'], axis=1)
        df_jpmorgan.to_csv(OUTPUT_DIR+'jpmorgan_US_engineer.csv')

    def tabulate_data(self):
        """Tabulates data by reading in csv file and outputting tabbed csv file."""
        print("Tabulating number of open job titles by city for JP Morgan...")
        df_jpmorgan = pd.read_csv(OUTPUT_DIR+'jpmorgan_US_engineer.csv')
        loc_tabbed = df_jpmorgan.groupby(["location_city", "location_state"]).size()
        df_jpmorgan_tabbed = pd.DataFrame(loc_tabbed)
        df_jpmorgan_tabbed.rename(columns={0: "num_job_openings"}, inplace = True)
        df_jpmorgan_tabbed.to_csv(OUTPUT_DIR+'jpmorgan_tabbed.csv')
        print("Here are the number of open job titles by city:")
        print(df_jpmorgan_tabbed)


class Google(Company):

    def get_url(self, url):
        """For a given job posting URL, returns the response object.
        Arguments:
        url -- URL to query
        """
        response = requests.get(url)
        return response

    def get_dataframe(self, num):
        """Takes list of Google jobs for a given page number and inserts it into a dataframe. Returns a dataframe.
        Arguments:
        num -- page number
        """
        num_str = str(num)
        # print(num_str)
        url = '''https://careers.google.com/api/jobs/jobs-v1/search/?company=Google&company=Google%20Fiber&company=YouTube&
                employment_type=FULL_TIME&hl=en_US&jlo=en_US&location=United%20States&page=''' + num_str + '&q=engineer&sort_by=relevance'
        response = self.get_url(url)
        jobs_json = response.json()['jobs']
        df = pd.DataFrame(jobs_json)
        return df

    def get_num_jobs(self):
        """Computes and returns the total number of jobs found."""
        url = '''https://careers.google.com/api/jobs/jobs-v1/search/?company=Google&company=Google%20Fiber&company=YouTube&
                employment_type=FULL_TIME&hl=en_US&jlo=en_US&location=United%20States&page=1&q=engineer&sort_by=relevance'''
        response = self.get_url(url)
        num_jobs = int(response.json()['count'])
        return num_jobs

    def scrape_data(self):
        """Scrapes data and outputs to csv file. """
        print("Scraping Google...")
        google = self.get_dataframe(1)
        num_jobs = self.get_num_jobs() # get total number of results
        num_pages = math.ceil(num_jobs/20)
        for i in range(2,num_pages+1):
            google = pd.concat([self.get_dataframe(i), google])
        google.to_csv(OUTPUT_DIR+'google.csv')
        print("Done scraping.")

    def clean_data(self):
        """Reads in csv, cleans data, and outputs to csv file."""
        print("Extracting Google US Engineering jobs...")
        df_google = pd.read_csv(OUTPUT_DIR+'google.csv')
        df_google = df_google[df_google['job_title'].str.lower().str.contains('engineer')] # get only titles with "engineer"
        df_google = df_google.reset_index()
        df_google = df_google.drop(['Unnamed: 0', 'index'], axis=1)
        df_google.to_csv(OUTPUT_DIR+'google_US_engineer.csv')

    def tabulate_data(self):
        """Tabulates data by reading in csv file and outputting tabbed csv file."""
        print("Tabulating number of open job titles by city for Google...")
        df_google = pd.read_csv(OUTPUT_DIR+'google_US_engineer.csv')
        location_lst = []
        for i in range(len(df_google)):
            loc_lst = ast.literal_eval(df_google.locations[i])
            for loc in loc_lst:
                location_lst.append(loc)
        loc_tabbed = pd.Series(location_lst).astype('str').value_counts()
        df_google_tabbed = pd.DataFrame(loc_tabbed)
        df_google_tabbed.rename(columns={0: "num_job_openings"}, inplace = True)
        df_google_tabbed.to_csv(OUTPUT_DIR + 'google_tabbed.csv')
        print("Here are the number of open job titles by city:")
        print(df_google_tabbed)


class HomeDepot(Company):

    def get_url(self, url):
        """For a given job posting URL, returns the beautiful soup object.
        Arguments:
        url -- URL to query
        """
        driver = webdriver.Chrome()
        driver.get(url)
        # Wait for page to load (code from: https://medium.com/the-andela-way/introduction-to-web-scraping-using-selenium-7ec377a8cf72)
        timeout = 5 # wait 5 seconds
        try:
            WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='jobTitle']")))
        except TimeoutException:
            print("Timed out waiting for page to load")
            driver.quit()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        return soup

    def get_list_text(self, original_list):
        """Gets the text from the html object"""
        return [i.get_text() for i in original_list] # uses list comprehensions!

    def get_dataframe(self, num):
        """Takes list of Google jobs for a given page number and inserts it into a dataframe. Returns a dataframe.
        Arguments:
        num -- page number
        """
        num_str = str(num)
        url = 'https://careers.homedepot.com/job-search-results/?keyword=engineer&location=United%20States&country=US&radius=15&pg=' + num_str
        soup = self.get_url(url)
        jobtitle_lst = self.get_list_text(soup.find_all(class_='jobTitle'))
        jobtype_lst = self.get_list_text(soup.find_all(class_='flex_column av_one_sixth', role='cell'))
        jobtype_lst = [x for x in jobtype_lst if x!='']
        jobcat_lst = self.get_list_text(soup.find_all(class_='flex_column av_one_fourth', role='cell'))
        location_lst = self.get_list_text(soup.find_all(class_='flex_column joblist-location av_one_sixth', role='cell'))
        df_homedepot = pd.DataFrame()
        df_homedepot['job_title'] = jobtitle_lst
        df_homedepot['location'] = location_lst
        df_homedepot['category'] = jobcat_lst
        df_homedepot['type'] = jobtype_lst
        return df_homedepot

    def get_num_pages(self):
        """Computes and returns the total number of pages found."""
        url = 'https://careers.homedepot.com/job-search-results/?keyword=engineer&location=United%20States&country=US&radius=15&pg=1'
        soup = self.get_url(url)
        num_results = int(soup.find(id = 'live-results-counter').get_text())
        total_num_pages = math.ceil(num_results/10)
        return total_num_pages

    def scrape_data(self):
        """Scrapes data and outputs to csv file. """
        print("Scraping Home Depot...")
        homedepot = self.get_dataframe(1)
        num_pages = self.get_num_pages()
        for i in range(2,num_pages+1):
            homedepot = pd.concat([self.get_dataframe(i), homedepot])
        homedepot.to_csv(OUTPUT_DIR+'homedepot.csv')
        print("Done scraping.")

    def clean_data(self):
        """Reads in csv, cleans data, and outputs to csv file."""
        print("Extracting Home Depot US Engineering jobs...")
        df_homedepot = pd.read_csv(OUTPUT_DIR+'homedepot.csv')
        df_homedepot = df_homedepot[df_homedepot['job_title'].str.lower().str.contains('engineer')] # get only titles with "engineer"
        df_homedepot = df_homedepot.reset_index()
        df_homedepot = df_homedepot.drop(['Unnamed: 0', 'index'], axis=1)
        df_homedepot.to_csv(OUTPUT_DIR+'homedepot_US_engineer.csv')

    def tabulate_data(self):
        """Tabulates data by reading in csv file and outputting tabbed csv file."""
        print("Tabulating number of open job titles by city for Home Depot...")
        df_homedepot = pd.read_csv(OUTPUT_DIR+'homedepot_US_engineer.csv')
        loc_tabbed = df_homedepot.location.value_counts()
        df_homedepot_tabbed = pd.DataFrame(loc_tabbed)
        df_homedepot_tabbed.rename(columns={0: "num_job_openings"}, inplace = True)
        df_homedepot_tabbed.to_csv(OUTPUT_DIR+'homedepot_tabbed.csv')
        print("Here are the number of open job titles by city:")
        print(df_homedepot_tabbed)
    

def main():
    microsoft = Microsoft().query()
    jpmorgan = Jpmorgan().query()
    google = Google().query()
    homedepot = HomeDepot().query()


if __name__ == '__main__':

    main()

