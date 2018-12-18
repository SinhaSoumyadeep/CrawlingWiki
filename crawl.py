import requests
import re
import time
import os
import enchant
from bs4 import BeautifulSoup

# This directory is used to keep track of the depth of the urls crawled from each seed
# and merge them into one single directory where the key is the depth and value is list of urls found at that depth.
mergedList = {}

#This the list of focus words.
focusedList = ["green"]

#This is the frontier which keeps track of all the URL's encountered thus far.
uniqueListOfUrl = []

#This is the List of urls crawled.
visited = []

#This is a temporary List which contains the urls encountered at a particular crawl.
depthInfoArray = []

#This is a dictonary which contains the list of urls for a particular seed
# where key is the depth and value is the list of urls at that depth.
poppedUrl = {}

#This is a flag which is set to true if we want to download the files again based on time.
timetoupdate = False

#This is a flag which is set to true if the files need to be downloaded if a copy does not exist.
saveHtmlFileFlag = False

#This is a flag which is set to true if we want to do a focused crawl.
focusedFlag = False

#This variable keeps track of the depth of a particular url.
depth = 1

#This is the maximum number of url that can be crawled.
maxUrl = 1000

#This is used to set the maximum depth of the urls that can be hit.
maxDepth = 6

#Set the timelapse before hitting another request.
politeness = 1


#This function is used to filter out keywords from the soup object.
def filter(soup, tag):
    for content in soup.find_all(tag):
        content.extract()
    return soup

#This function is used to hit request to a particular page
# and returns a soup object and save the raw html pages if the write flag is set to true.
def getPage(url, writeFlag):
    time.sleep(politeness)
    soup = None
    try:
        page = requests.get(url)

        if page.status_code != 200:
            return soup
        soup = BeautifulSoup(page.content, 'html.parser')


        if writeFlag != "":
            saveHtmlFiles(soup, url, writeFlag)

    except:
        soup = None

    return soup

#This function is used to download the raw html and save it in a file.
def saveHtmlFiles(soup, url, writeFlag):

    fileName = getfilename(url)

    directory = "files/DownloadHTML"
    if not os.path.exists(directory + "/" + writeFlag):
        os.makedirs(os.path.join(directory, writeFlag))

    filepath = directory + "/" + writeFlag + "/" + fileName

    f = open(filepath, "w")
    f.write(str(soup))

#This function is used to match the url with the url
# then making sure that the url makes sense within the context of the focused Key word.
def checkForKey(url,link):

    page = getfilename(url)
    keysList = re.split("[\W|_]",page)+re.split(" ",link.text)

    for tags in keysList:
        for focusedKeySearch in focusedList:
            regex = r"[\W]*\b"+focusedKeySearch+".*"
            matches = re.match(regex, tags, re.IGNORECASE)
            if matches:
                d = enchant.Dict("en_US")
                if d.check(matches.group()):
                    return True

    return False



#This function is used to crawl and validate the urls encountered
# and checks if the url hit can only be of the maximum depth set.
def crawl(link_url):
    print("********* ", link_url, " IS GETTING CRAWLED ************\n")

    global depth

    for key in poppedUrl:
        if link_url in poppedUrl[key]:
            depth = key
            break

    depth = depth + 1


    if depth <= maxDepth:

        depthInfoArray.clear()

        filtertag = ["table", "img"]

        soup = getPage(link_url, "");
        if soup == None:
            return

        soup = extractbodytag(soup)

        for tag in filtertag:
            soup = filter(soup, tag)

        for link in soup.find_all('a'):
            url = str(link.get('href'))
            url = addDomain(url)
            if (isValidUrl(url)):
                if "disambiguation" not in url and \
                        "#" not in url and \
                        ".jpg" not in url and \
                        ".png" not in url and \
                        ".pdf" not in url and \
                        "Main_Page" not in url and\
                        not checkForColon(url):

                    if focusedFlag:
                        if checkForKey(url,link):
                            #print(link.text, '    ', url)
                            orderedUniqueList(url)
                    else:
                        orderedUniqueList(url)


        # print(depth, " ", depthInfoArray)

        if depth not in poppedUrl.keys():
            poppedUrl[depth] = depthInfoArray.copy()
        else:
            temp = poppedUrl[depth]
            mergedList = temp + depthInfoArray.copy()
            poppedUrl[depth] = mergedList

        # print("\n\n\n\n")

#This function is used to extract the Body of the Html page.
def extractbodytag(soup):
    for content in soup.find_all("body"):
        soup = content.extract()
    return soup

#This function is used to implement the breath first search algorithm.
def bfs(seed):
    if visited.__len__() >= maxUrl:

        return
    visited.append(seed)
    crawl(seed)
    if(uniqueListOfUrl.__len__() == 0):
        return
    newseed = uniqueListOfUrl[0]
    uniqueListOfUrl.remove(newseed)
    bfs(newseed)

#This function is used to print the Urls crawled.
def printurl():
    count = 0
    for key in poppedUrl:
        for url in poppedUrl[key]:
            if count != maxUrl:
                print(url)
                count += 1

#This function is passed a filename and writes the url to a file.
def writefile(filename):
    directory = "files"
    htmldirectory = directory+"/DownloadHTML"
    if not os.path.exists(directory):
        os.mkdir(directory)

    f = open(directory + "/" + filename, "w")
    count = 0
    for key in poppedUrl:
        for url in poppedUrl[key]:
            if count != maxUrl:


                if saveHtmlFileFlag:
                    filename1 = "['" + getfilename(poppedUrl[1])

                    htmlfileName = getfilename(url)

                    filepath = htmldirectory + "/" + filename1 + "/" + htmlfileName

                    if not os.path.exists(filepath) or timetoupdate:
                        print("fetching the  html of url    ", filepath,"   ",timetoupdate)
                        getPage(url, filename1)
                    else:
                        print("file exists and its not time to update so not downloading ", filepath," ",timetoupdate)


                f.write(url + "#" + str(key) + "\n")
                count += 1

#This function is used to fetch the filename by splitting the url.
def getfilename(path):
    fileurl = str(path).split("/")
    filename = fileurl[fileurl.__len__() - 1]
    return  filename


#This function adds unique url to a list.
def orderedUniqueList(input):
    if input.upper() not in (url.upper() for url in uniqueListOfUrl):
        if input.upper() not in (url.upper() for url in visited):
            uniqueListOfUrl.append(input)
            depthInfoArray.append(input)


#This function adds domain name to the list of urls.
def addDomain(link):
    p = re.compile("^/wiki/(.)*")
    m = p.match(link)

    if m:
        return "https://en.wikipedia.org" + link
    else:
        return link

#This function is used to filter out urls with ":".
def checkForColon(link):
    p = re.compile("https://en.wikipedia.org/wiki/(.)*:(.)*")
    m = p.match(link)
    if m:
        return True
    else:
        return False

#This function is used to validate urls and filter out external links.
def isValidUrl(str):
    p = re.compile("https://en.wikipedia.org/wiki/(.)*")
    m = p.match(str)
    if m:
        return True
    else:
        return False

#This function resets all the variables, lists and dictionary to its initial value.
def resetEverything():
    global depth
    global timetoupdate
    global saveHtmlFileFlag
    global focusedFlag
    global focusedKeySearch
    poppedUrl.clear()
    uniqueListOfUrl.clear()
    visited.clear()
    depthInfoArray.clear()
    poppedUrl.clear()
    depth = 1
    focusedKeySearch = ""

#This function is used to split the url into depth and url.
def splitUrlAndDepth(url):
    return url.replace("\n","").split("#")

#This function is used to remove duplicates from the Merged list.
def findDuplicateUrlInMergedFile(url,depth):

    removeIncomingUrl = False
    for key in mergedList.keys():
        if url in mergedList[key]:
            if key > depth:
                mergedList[key].remove(url)
            else:
                removeIncomingUrl = True

    if removeIncomingUrl == False:
        mergedList[depth].append(url)


#This function is used to merge the urls from all different seeds.
def mergeListFunc(filename):
    fileContent = open("files/"+filename, "r")

    for line in fileContent:

            splitlink = splitUrlAndDepth(line)
            url = splitlink[0]
            depth = splitlink[1]
            if splitlink[1] not in mergedList:
                mergedList[depth] = []
            findDuplicateUrlInMergedFile(url, depth)


    f = open("files/" + "mergedFile", "w")
    count = 0
    for key in mergedList.keys():
        for url in mergedList[key]:
            if count < maxUrl:
                f.write(url + "\tdepth:" + str(key) + "\n")
                count += 1

#This is function is used crawl list of seeds.
def task1():
    global focusedFlag
    global mergedList
    focusedFlag = False
    resetEverything()
    seeds = ["https://en.wikipedia.org/wiki/Time_zone", "https://en.wikipedia.org/wiki/Electric_car",
             "https://en.wikipedia.org/wiki/Carbon_footprint"]
    for seed in seeds:
        fileName = getfilename(seed)
        resetEverything()
        poppedUrl[1] = [seed]
        bfs(seed)
        writefile(fileName)
        printurl()
        mergeListFunc(fileName)

    #print(mergedList)
    resetEverything()

#This function is used to implement focused crawling.
def focusedCrawling():
    global focusedFlag
    global focusedKeySearch
    resetEverything()
    focusedFlag = True
    focusedUrl = "https://en.wikipedia.org/wiki/Carbon_footprint"
    #for focusedKey in focusedList:
    resetEverything()
    #focusedKeySearch = focusedKey
    fileName = "focusedFile"
    poppedUrl[1] = [focusedUrl]
    bfs(focusedUrl)
    writefile(fileName)
    printurl()
    resetEverything()


#This is the main function.
def main():
    task1()
    focusedCrawling()










main()
