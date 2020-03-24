#!/usr/bin/env python3
"""
Reddit Wallscraper
Course: CS 41
Name: Danny Du
SUNet: dannydu

This is a wallpaper scraping program that queries data from certain subreddits.
"""
import wallscraperutils as utils
import requests
import json
import sys
import os

BASE_URL = 'https://reddit.com/r/'


class RedditPost:
    def __init__(self, data):
    	self.ok = True

        #essential information
    	self.title = data['title']
    	self.img_url = data['url']
    	self.author = data['author']
    	self.post_hint = data['post_hint']
    	self.extension = '.' + self.img_url.split('.')[-1]

        #checks for unknown formats
    	if len(self.extension) != 4:
    		self.ok = False 

        #resolution-related properties
    	self.width = data['preview']['images'][0]['source']['width']
    	self.height = data['preview']['images'][0]['source']['height']
    	self.aspect_ratio = utils.get_aspect_ratio(self.width, self.height)

        #score-related properties
    	self.score = data['score']
    	self.ups = data['ups']
    	self.downs = data['downs']
    	self.num_comments = data['num_comments']

        #other
    	self.media = data['media']
    	self.is_video = data['is_video']
    	self.json_data = data


    def add_x(self, num1, num2):
        #concatenates two items together in their string form, with an 'x' in the middle
    	return str(num1) + 'x' + str(num2)

    def download(self):
    	if self.ok:

    		aspect_ratio_path = 'wallpapers/' + self.add_x(*self.aspect_ratio) + '/'
    		resolution_path = aspect_ratio_path + self.add_x(self.width, self.height) + '/'

            #create new directories if necessary in accordance to aspect ratio and resolution
    		if not os.path.isdir(aspect_ratio_path):
    			os.mkdir(aspect_ratio_path)
    		if not os.path.isdir(resolution_path):
    			os.mkdir(resolution_path)

            #makes request to url of the image
    		img = requests.get(self.img_url)

            #write the image locally
    		file_path = resolution_path + self.title + self.extension
    		if not os.path.isfile(file_path):
    			with open(file_path, 'wb') as f:
    				f.write(img.content)
    				return True
    		else:
    			print('whoops, that image already exists!')
    	else:
    		print('whoops, that\'s not an image!')
    	return False

    def name(self):
    	return self.title

    def __str__(self):
        return self.title + ' (' + str(self.score) + '), posted by: ' + self.author +', post_hint: ' + str(post_hint)

    
def query(to_query):
	try:
		response = requests.get(
			BASE_URL + to_query + '/.json',
			headers={'User-Agent': 'Wallscraper Script by @dannydu'}
		)
    #catchs connection error in case of failed internet
	except requests.ConnectionError:
		print('no internet connection!')
		return -1

	if response.status_code == 404:
		print('page not found!')
		return -1

    #if the request was successful
	if response.status_code == 200 and response.ok:
		data = response.json()['data']['children']
		if len(data) == 0:
			print('subreddit empty/not found!')
			return -1
	else:
		print('reddit has responded with error code: ', response.status_code)
		return -1

	return data

    
def main():
    #command line functionality
	if len(sys.argv) == 1:
		subreddit = 'wallpapers'
	else:
		subreddit = sys.argv[1]

    #makes query
	query_data = query(subreddit)
    #if anythign wrong with query, gracefully exit program with error code -1
	if query_data == -1:
		print('exiting now')
		return -1

    #converts relevant python dictionaries into RedditPost objects
	posts = [RedditPost(x['data']) for x in query_data if 'preview' in x['data']]

    #download the images themselves
	num_downloaded = 0
	for post in posts:
		print('downloading ' + post.name() + "... ", end='')
		if post.download():
			num_downloaded += 1
			print('done!')
	print('images downloaded: ', num_downloaded, ' (of {} total)'.format(len(posts)) )

if __name__ == '__main__':
    main()
