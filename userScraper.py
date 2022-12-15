# Importing libraries
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import cloudscraper

 
oldContent = ""
oldUsername = "SensualLove"
# Making a GET request
# playsound('C:/Users/Jack Bowman/Documents/Programs/PytScripts/Watcher/beep-07a.wav')
headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36",
            'referer': 'https://magiceden.io/',
             'accept': 'application/json'}
session = cloudscraper.create_scraper(browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    })
# get all the users from the page according to page number
def getPage(pageNum):
    r = session.get('https://tracker.gg/for-honor/leaderboards/stats/all/KdRatioP?gameType=pvp&type=stats&page=' + str(pageNum),headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    file = open("testfile.html","w")
    file.write(soup.prettify())
    file.close()

    return soup.find_all(class_="username")



# get and parse all the users from pages 1 to 2368
for i in range(1,2465):
    # failed at 938
    users = getPage(i)
    
    # every page has 100 users. if the length of users is not 100 somthing has gone wrong
    # try waiting 10, 20, 30 ect until you get back
    waitTime = 10
    while(len(users) != 100):
        print("ERROR at page " + str(i) + " : " + str(len(users)))
        # playsound('C:/Users/Jack Bowman/Documents/Programs/PytScripts/Watcher/beep-07a.wav')
        time.sleep(waitTime)
        # waitTime += 10
        users = getPage(i)

    j=0
    file = open("usersTesting10-18-1.txt","a")
    for user in users:
        j+=1
        # funny html spaghetti parsing
        file.write(str(user.contents[0].contents[0]["href"]) + "\n")
        print(str(j) + ": " + user.contents[0].contents[0]["href"])
    file.close()

    print(i)
    time.sleep(1)
    # if(i%100 == 0):
    #     time.sleep(60)


