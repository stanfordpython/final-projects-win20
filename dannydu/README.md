# CS 41 Final Project - Wallscraper

This is a Wallscraper script that was written based on the instructions from lab 5. Two extensions were implemented, command line arguments are enabled and the plist file to run the script every day using launchd is included in the github repo as well as final submission.

## Required Packages

* `os`, `sys` from Python standard library
* `requests`, `json`

## Code Design

The basic design of this wallscraper application follows in line with the provided starter code on this repo: https://github.com/stanfordpython/python-labs/blob/master/notebooks/lab-5/wallscraper-notebook.ipynb.

### Main

The main function takes in any command line arguments provided as the subreddit to access, defaulting to `r/wallpapers` if none is provided. Main will then query the website via the `Query` function (see below), implemented using requests. Once `Query` returns the data for all posts in the subreddit, it will convert each post's `.json` data into the `RedditPost` class. Finally, main will download all the `RedditPost` objects that are images, counting in the process how many images there are and reporting back to the user (via print) the status of each post (downloaded/duplicate/non-image).

### Query

The `Query` function uses the requests library to make a query to the desired subreddit. It has appropriate error handling in the cases of no internet connection and subreddit not found. It will return all of the posts found in the subreddit in the form of an array of python dictionaries derived from the `.json` obtained from reddit.

### RedditPost (class)

This class is responsible for representing a single post. In the constructor, a dictionary is taken and all relevant information is placed into private variables per that object. The core functionality of the class comes in the function `download`, which determines whether a post is of an appropriate format to be downloaded and proceeds to write it into the local `wallpapers` directory, creating whichever subdirectories are needed according to the aspect ratio and resolution of the image.

## Using the Script

Run the script while operating on the cs41 class environment (python 3.8) using

```
python wallscraper.py
```

By default, the script will scrap data from r/wallpapers. However, via command line arugments, you can access image data from other subreddits

```
python wallscraper.py teslamotors
```

In order to use the provided `plist`/`launchd` script, move the provided `.plist` file into `~/Library/LaunchAgents`. Edit the contents in the file to be consistent with where you have the scripts on your local computer. Then, use the following lines of code to begin running the script in the background.

```
launchctl load ~/Library/LaunchAgents/com.cs41.wallscraper.plist
launchctl start com.cs41.wallscraper.plist
```

Other useful functions regarding `launchd`:

```
launchctl unload ~/Library/LaunchAgents/com.cs41.wallscraper.plist
launchctl stop com.cs41.wallscraper.plist
launchctl list | grep cs41
```

## Authors

* **Danny Du** - dannydu@stanford.edu

## License

This project is licensed under the MIT License.

## Acknowledgments

* CS 41 instructors for the lab instructions
* Nathan Grigg (https://nathangrigg.com/) and his post on launchd (https://nathangrigg.com/2012/07/schedule-jobs-using-launchd)