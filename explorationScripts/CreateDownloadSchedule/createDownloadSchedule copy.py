import sqlite3
import json
import time


getNamesSQL = """
SELECT username,platform,MAX(UTCSeconds)
FROM stat
GROUP BY username,platform
"""

DAY = 86400

conn = sqlite3.connect("FH.db")
crsr = conn.cursor()
crsr.execute(getNamesSQL)
ans = crsr.fetchall()

file = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\downloadSchedule\\DownloadedNames1231.json","r")
lastDownloaded = json.load(file)
file.close()

userFile = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\compiledUsers-12-04-1.csv","r")
usersFileLines = userFile.readlines()
userFile.close()
allUsers = {}


for line in usersFileLines:
    splitLine = line.split(",")
    platform = splitLine[0]
    username = splitLine[1][0:-1]
    splicedUsername = username.split("%20")
    splicedUsername = " ".join(splicedUsername)
    allUsers[splicedUsername + "," + platform] = 1


downloadSchedule = {}


counter = 0
for userKey in allUsers:
    if userKey not in lastDownloaded:
        counter += 1
        downloadSchedule[userKey] = time.time()
print(counter)
print(len(allUsers))
for user in ans:
    username = user[0]
    platform = user[1]
    lastUpdate = user[2]
    userKey = username + "," + platform 
    try:
        netTimeBetweenDownloadAndUpdate = lastUpdate - lastDownloaded[userKey]
        if netTimeBetweenDownloadAndUpdate < DAY * 3:
            downloadSchedule[userKey] = time.time() + (DAY * 7)
        elif netTimeBetweenDownloadAndUpdate < DAY * 30:
            downloadSchedule[userKey] = time.time() + (DAY * 7)
        elif netTimeBetweenDownloadAndUpdate < DAY * 60:
            downloadSchedule[userKey] = time.time() + (DAY * 14)
        else:
            downloadSchedule[userKey] = time.time() + (DAY * 30)
    except:
        ...


counter = 0
for player in downloadSchedule:
    if downloadSchedule[player] > time.time():
        counter += 1
print(counter)

file = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\downloadSchedule\\downloadSchedule.json","w")
json.dump(downloadSchedule,file)
file.close()


    



