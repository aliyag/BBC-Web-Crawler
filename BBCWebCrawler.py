

import urllib2
from bs4 import BeautifulSoup
import Queue
import sys
import re
import csv



# Formats the link, if valid link, adds to queue
def addLinkToQueueIfValid(link):
    # add http:// so that link can be opened
    if link.startswith("//"):
        link = "http:" + link
    # RELATIVE LINK: modifies relative link to absolute format
    elif link.startswith("/"):
        link = "http://bbc.com" + link
    # checks if fits requirements before putting in the queue
    regexp = re.compile(r"https?:\/\/www.bbc")
    if regexp.search(link) and not isLinkinQueue(link):
        prevAddedToQueue[link] = ""
        links.put(link)

# checks if link with http or https is in queue
def isLinkinQueue(link):
    if link.startswith("https"):
        # make link to https
        if link in prevAddedToQueue or link.replace("https", "http") in prevAddedToQueue:
            return True
    elif link.startswith("http"):
        # check if https in dictionary
        if link in prevAddedToQueue or link.replace("http", "https") in prevAddedToQueue:
            return True
    return False

# Checks if language is English, if true, finds headline and corresponding section
def printHeadlineIfEnglish(language):
    # if page has language tag
    if language != None:
        # checks if English
        if language.get("lang") == "en-GB" or language.get("lang") == "en":
            # finds article title and article section
            section = soup.find("meta", property="article:section", content=True)
            title = soup.find("meta", property="og:title", content=True)
            if section and title:
                print title["content"] + "," + section["content"], url

# while loop that stops if queue is empty or reached 10,000 links
while not emptyQueue:
    # BOOLEAN TO CHECK IF LINK IS VALID
    newLink = False
    # GET NEXT LINK FROM QUEUE
    # while loop that aids in getting next link or checks if the queue is empty
    while not newLink:
        # IF QUEUE IS EMPTY
        if links.empty():
            # NOTIFY THE USER
            print "the queue is empty"
            # SET EMPTYQUEUE BOOLEAN AS TRUE, the program stops
            emptyQueue = True
        else:
            # GET A NEW LINK
            url = links.get()
        try:
            # get the html code using python library
            html = urllib2.urlopen(url)
            # SET NEWLINK BOOLEAN AS TRUE AND USE THE LINK
            newLink = True
            # get a new link, go through the same tests
        except:
             pass

    # create a soup object to get tags
    soup = BeautifulSoup(html, "html.parser")

    for link in soup.find_all('a'):
        link = str(link.get('href'))
        addLinkToQueueIfValid(link)

    language = soup.find("html", attrs={"lang": True})
    printHeadlineIfEnglish(language)
