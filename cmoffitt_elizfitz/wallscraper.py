#!/usr/bin/env python3
"""
Reddit Wallscraper
Course: CS 41
Name: Chris Moffit and Elizabeth Fitzgerald
SUNet: cmoffitt and elizfitz

Replace this with a description of the program.
"""
# import utils
import requests
import sys
import re
import os
import pickle

#Uses requests module to query reddit for json file corresponding to subreddit
def query(subreddit):
    URL_START = "https://reddit.com/r/"
    URL_END = ".json"
    url = URL_START + subreddit + URL_END
    print(url)
    headers = {'User-Agent': "Wallscraper Script by @cmoffitt"}
    r = None

    # Make request and catch exceptions
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting: No internet connection")
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
        sys.exit(1)

    # Capture json dict object of subreddit if response was successful
    print(r)
    if r.ok:
        json_data = r.json()
    else:
        print("The server did not return a successful response. Please try again")
        sys.exit(1)

    # Check if valid subreddit
    if not isValidSubreddit(json_data):
        print("Not a valid subreddit. Please try again.")
        sys.exit(1)
 
    return json_data

#Class defining one reddit post
class RedditPost:
    #Initializes one reddit post as a dictionary storing certain attributes from the json post object
    def __init__(self, data):
        post_data = data
        attr = ["subreddit", "is_self", "ups", "post_hint", "title", "downs", "score", "url", "domain", "permalink", "created_utc", "num_comments", "preview", "name", "over_18"]

        dict = {}
        for k in attr:
            try:
                dict[k] = post_data["data"][k]
            except:
                dict[k] = None

        self.data = dict

    #Downloads the post image to a file on the computer, preventing duplicate image downloading
    def download(self):
        if ".jpg" in self.data["url"] or ".png" in self.data["url"]: #only download if it actually is an image
            #format the correct name and path for the file
            name = re.sub(r'\[.*\]', '', self.data["title"])
            name = re.sub(" ", "", name)
            name = re.sub(r'[^a-zA-Z0-9]', "", name)
            path = "wallpapers/" + str(self.data["preview"]["images"][0]["source"]["width"]) + "x" + str(self.data["preview"]["images"][0]["source"]["height"]) + "/"
            filename = name + ".png"

            if not os.path.exists(path):
                os.makedirs(path)

            img_data = requests.get(self.data["url"]).content #unique info regarding the particular image to save in order to prevent duplicate image downloading

            #Run this code the first time in order to create the pickle file for seen_wallpapers
            #seen_wallpapers.append(img_data)
            #f = open("seen_wallpapers.pickle", 'wb')
            #pickle.dump(seen_wallpapers, f)
            #f.close()

            #upload seen_wallpapers pickle file to compare against img_data and prevent duplicae image downloading
            seen_wallpapers = []
            f = open("seen_wallpapers.pickle", 'rb')
            seen_wallpapers = pickle.load(f)
            f.close()
            if img_data not in seen_wallpapers:
                seen_wallpapers.append(img_data)
                f = open("seen_wallpapers.pickle", 'wb')
                pickle.dump(seen_wallpapers, f)
                f.close()
                #save image in file
                with open(os.path.join(path, filename), 'wb') as temp_file:
                    temp_file.write(img_data)
                    temp_file.close()

        else:
            pass

    def __str__(self):
        #"RedditPost({title} ({score}): {url})
        string = "RedditPost({" + self.data["title"] + "} ({" + str(self.data["score"]) + "}): {" + self.data["url"] + "})"
        return string



# Checks if valid subreddit by making sure json dict object is properly filled with contents
def isValidSubreddit(json_data):
    if json_data['data']['dist'] == 0:
        return False
    else:
        return True


def main(subreddit):
    q = query(subreddit)

    children = (q['data']['children'])
    postCount = 0  # To confirm we have all 25 "posts"
    scoreCount = 0  # To check number of posts with a score above 500

    RedditPosts = [RedditPost(post) for post in children]

    for post in RedditPosts:
        new_post = post
        postCount += 1
        if new_post.data["score"] > 500:
            scoreCount += 1
        post.download()

    print("There were " + str(postCount) + " posts.")
    print(str(scoreCount) + " of those posts had a score over 500.")

if __name__ == '__main__':
    main(sys.argv[1])
