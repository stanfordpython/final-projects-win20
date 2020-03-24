# CS 41 Final Project: Tweet Sentiment Analysis

#### Contributors: Erick Hernandez and Ruben Sanchez

## Functionality

This project implements a tweet sentiment aggreator tool that can be run as a python executable. It will take in input that provides the hashtag we would like to search for and the keywords we would like to seperate by under that hashtag.

From there, the program will aggregate tweets and do sentiment analysis on them by displaying a graph as shown below. 

![Sample photo](./sample.png)

This graph was created by searching the hashtag "COVID19" and has keyworsds, China, US, Italy, Trump.

## Usage

1) The first step is creating/using the provided config file to configure your search results.

edit `config.yaml` to look something like:
```
hashtag: COVID19
keywords: 
  - China
  - US
  - Italy
  - Trump
```
or 
```
hashtag: DemDebate
keywords: 
  - Clinton
  - Bernie
  - Biden
  - Bloomberg
```
2) You can run the script by providing the name of the config file with the `-f` flag, e.g. 
```
12:04 PM (pyvenv) $ python sentiment.py -f config.yaml
```

## Bugs

We currently do not have any bugs that we have found. Our biggest issue that we are currently limited to a small number of tweets because the twitter API only allows us to query 18k tweets per minute. The downloading is very slow and we are not able to break into shorter time intervals.

## Contact
Please contact:
- rubensan [at] stanford [dot] edu 
- erickha [at] stanford [dot] edu 
