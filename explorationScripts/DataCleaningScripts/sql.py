import sqlite3
from bs4 import BeautifulSoup
import cloudscraper
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

conn = sqlite3.connect("FH.db")
crsr = conn.cursor()
sql = """

SELECT * from stat where username = 'alpha'

"""

crsr.execute(sql)
ans = crsr.fetchall()

print(ans,len(ans))

users = getPage(1322)
j = 0
for user in users:
    j+=1
    # funny html spaghetti parsing
    print(str(j) + ": " + user.contents[0].contents[0]["href"])