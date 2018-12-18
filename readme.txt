
USE PYTHON 3.6 to run the code
*************************************************************************************************
Libraries(Packages) to be imported(installed)
1)beautifulSoup 
  pip install beautifulSoup4
2)requests
  (package already present in Python 3.6)
  pip install requests
3)time
  (package already present in Python 3.6)
4) re
   (package already present in Python 3.6)
5) enchant
   pip install pyenchant
6)os
	(package already present in Python 3.6)

*************************************************************************************************
Instruction for Running crawl.py
1) Use Python 3.6 to run the code.
2) Create a new Project in Pycharm (Or any Python IDE)
3) Create a new python file in the project (name it Task_1.py)   
4) Copy Paste the code from  "crawl.py" in submitted folder into the python file(Task_1.py).
5) Run the Task_1.py.
6) Code will generate 5 files (seed1).txt, (seed2).txt, (seed3).txt, mergedFile.txt, focusedFile.txt which will contain the urls crawled for seed 1, seed 2, seed 3, mergedFile which is a Consolidate list	obtained from all three	crawls into	one	list of	unique URLs and follows the same order of link importance, focusedFile which includes the list of urls that contains the keyword(s) that is passed during the crawl.

*************************************************************************************************
Task 1.
	Task 1 takes 3 seeds 
		"https://en.wikipedia.org/wiki/Time_zone"
		"https://en.wikipedia.org/wiki/Electric_car"
        "https://en.wikipedia.org/wiki/Carbon_footprint"

     and crawls through the aforementioned urls and search for urls in the crawling page using BFS.
     various filters are used to extract the body of the Raw html file and removal of the external links, administrative links and redirect links while ignoring Tables, Formulas, Image files and NonTextual media. 
     The crawler is set to crawl a certain depth which can be set explicitly. Currently it is set to 6 which means that the crawler will visit/crawl only those URL whose depth is 6 or below 6.There is another flag "saveHtmlFileFlag" which can be set to "True" if the Raw HTML text of the crawled Url needs to be downloaded. The program is coded in such a way that 
     if the Raw HTML text are already downloaded and the "timeToUpdate" is set to "False" then the files are not downloaded all over again when the program is run next time. However, if the "timeToUpdate" flag is set to "True" then the file is downloaded again even if the files are already downloaded. The timeToUpdate can be set to "True" or "False" based on time elapsed which can be a future enhancement to this project. The program can also handle redirected urls and not include those urls in the file. The program checks for the status returned from the request made and only include the link if the status returned is 200. The dulicate urls are also not allowed to be insered in the list thus maintaining unique list of urls. Once the list is formed of the unique urls then write it to a file in formal url#depth.

Maximum depth reached: 3

*************************************************************************************************
Task 2.
	To merge the urls, the 3 files generated from Task 1 is read which includes the URL and the depth associated with the URL.
	each and every line is read and split in to the url and the depth and accordingly included in the dictionary which has key as the depth and the value as the list of urls. Thus, urls from depth 1 from each files will be merged and saved as a list of urls for depth one and so on. The overlapping urls which can be encountered in the 3 files are also handeled by either removing or inserted based on priority. Thus, for example url enountered at level 1 in given priority over the same url which is encountered at some another level in another seed list. Thus removing duplicates from the list. Once the list is formed then the url is written into a file called "meregedFile"

Maximum depth reached: 3
*************************************************************************************************
Task 3.
	The focused keyword is "green" and the Seed url is "https://en.wikipedia.org/wiki/Carbon_footprint"
	The url is split into individual words based on regular expression that checks for non alpha numeric character and "_".
	the text of the anchor tag is also taken into consideration which is split into words using space and then the entire word set is checked with the regular expression which looks for the focused word or similar word. Once its a match it is then checked in the pyenchant dictionary to make sure that the word matched makes sense. If these requirements are fulfilled then the url is added to the list. 

Maximum depth reached: 6
*************************************************************************************************
Details:
	The Algorithm used is BFS, which will take seed as an argument and explores all of the neighbor nodes at the present depth prior to moving on to the nodes at the next depth level. Thus, the links encountered closer to the title within an article are deemed more important and hence those pages are	acquired prior to ones occurring later in the article. 



*************************************************************************************************
Reference:
https://www.dataquest.io/blog/web-scraping-tutorial-python/
https://stackoverflow.com/questions/35757407/how-to-add-dictionary-to-pyenchant
https://www.pythonforbeginners.com/os/pythons-os-module
https://docs.python.org/3/tutorial/index.html
