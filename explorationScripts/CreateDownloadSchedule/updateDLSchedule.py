import sqlite3
import json
import time
import random

def updateUser(lastUpdatedDate,lastDownloadDate):
    diff = lastDownloadDate - lastUpdatedDate
    if diff > DAY * 40:
        return random.randint(int(time.time()) + DAY * 7, int(time.time() + DAY * 60))
    else:
        return random.randint(int(time.time()) + DAY * 7, int(time.time() + DAY * 14))
    

getNamesSQL = """
SELECT username,platform,MAX(UTCSeconds)
FROM stat
GROUP BY username,platform
"""


DAY = 86400

print("getting last updates...")
conn = sqlite3.connect("FH.db")
crsr = conn.cursor()
crsr.execute(getNamesSQL)
ans = crsr.fetchall()
print("parsing...")
mostRecentUpdates = {}
for user in ans:
    mostRecentUpdates[user[0] + "," + user[1]] = user[2]


file = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\downloadSchedule\\DownloadedNames1231.json","r")
lastDownloaded = json.load(file)
file.close()

# userFile = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\compiledUsers-12-04-1.csv","r")
# usersFileLines = userFile.readlines()
# userFile.close()
# allUsers = {}

file = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\downloadSchedule\\downloadSchedule.json","r")
downloadSchedule = json.load(file)

print("updating...")
for user in lastDownloaded:
    lastUpdateDate = mostRecentUpdates[user]
    lastDownloadDate = lastDownloaded[user]
    downloadSchedule[user] = updateUser(lastUpdateDate,lastDownloadDate)
    
    



file = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\downloadSchedule\\downloadSchedule.json","w")
json.dump(downloadSchedule,file)
file.close()


    



