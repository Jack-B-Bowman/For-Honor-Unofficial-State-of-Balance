import json
from unicodedata import name
import matplotlib.pyplot as plt
import numpy as np

import seaborn as sns

import sqlite3
conn = sqlite3.connect("FH.db")
crsr = conn.cursor()
mode = "Dominion"
sqlMode = f"""select 
	   name,
	   username,
	   platform,
       UTCSeconds,
	   wins,
	   losses,
       reputation
from (
  select 
		 name,
		 username, 
		 platform,
         UTCSeconds,
         max(UTCSeconds) over (partition by username,platform) as max_date,
		 min(UTCSeconds) over (partition by username,platform) as min_date,
		 wins,
		 losses,
         reputation
  from (SELECT mode.name,mode.wins,mode.losses, stat.username, stat.platform, stat.UTCSeconds, stat.reputation FROM mode INNER JOIN stat on mode.playerID = stat.playerID  WHERE mode.name = '{mode}')
)
where UTCSeconds = max_date OR UTCSeconds = min_date
ORDER BY username"""

sqlTotal = """select 
	   username,
	   platform,
       UTCSeconds,
	   wins,
	   losses,
	   reputation
from (
  select 
		 
		 username, 
		 platform,
         UTCSeconds,
         max(UTCSeconds) over (partition by username,platform) as max_date,
		 min(UTCSeconds) over (partition by username,platform) as min_date,
		 wins,
		 losses,
		 reputation
  from stat
)
where UTCSeconds = max_date OR UTCSeconds = min_date
ORDER BY username"""

crsr.execute(sqlMode)

ans = crsr.fetchall()

activeUsers = {}
counter = 0
for i in range(len(ans)):
    counter += 1
    if counter % 1000 == 0:
        print(f"entries parsed: {counter}")
    mode = ans[i][0]
    user = ans[i][1]
    platform = ans[i][2]
    time = ans[i][3]
    wins = ans[i][4]
    losses = ans[i][5]
    reputation = ans[i][6]
    if user in activeUsers:
        if platform in activeUsers[user]:
            stat = {
                "time" : time,
                "wins" : wins,
                "losses" : losses,
                "mode" : mode,
                "platform" : platform,
                "reputation": reputation
            }          
            activeUsers[user][platform].append(stat)
        else:
            stat = {
                "time" : time,
                "wins" : wins,
                "losses" : losses,
                "mode" : mode,
                "platform" : platform,
                "reputation": reputation
            }          
            activeUsers[user][platform] = [stat]
    else:
        stat = {
                "time" : time,
                "wins" : wins,
                "losses" : losses,
                "mode" : mode,
                "platform" : platform,
                "reputation": reputation
        } 
        activeUsers[user] = {}
        activeUsers[user][platform] = [stat]


PSNstats = []
XboxStats = []
PCstats = []

# file = open("updatedUserStats05-18-2.json","r")
# activeUsers = json.load(file)

totalMatchesPC = 0
totalUsersPC = 0
totalMatchesPSN = 0
totalUsersPSN = 0
totalMatchesXBL = 0
totalUsersXBL = 0

numOver60 = {"xbl" : 0,
                 "psn" : 0,
                 "uplay": 0
                 }

percenters50 = {}

numUsers = 0

for user in activeUsers:
    for platform in activeUsers[user]:
        if len(activeUsers[user][platform]) > 1:
            stats = activeUsers[user][platform]
            newlist = sorted(stats, key=lambda d: d['time'])
            first = newlist[0]
            last = newlist[-1]

            # wins = last["wins"] - first["wins"]
            # losses = last["losses"] - first["losses"]
            wins = first["wins"]
            losses = first["losses"]
            if wins + losses > 10:

                winRate = (wins/(wins + losses)) * 100

                if winRate < 1:
                    print(user)

                if(winRate < 101):
                    userTuple = (last["reputation"],winRate)
                    numUsers += 1
                    if last["platform"] == "psn":
                        PSNstats.append(userTuple)
                        totalUsersPSN += 1
                        totalMatchesPSN += wins + losses
                    if last["platform"] == "xbl":
                        XboxStats.append(userTuple)
                        totalUsersXBL += 1
                        totalMatchesXBL += wins + losses
                    if last["platform"] == "uplay":
                        PCstats.append(userTuple)
                        totalUsersPC += 1
                        totalMatchesPC += wins + losses

totalUsers = totalUsersPC + totalUsersPSN + totalUsersXBL
pcPercent = (totalUsersPC / totalUsers) * 100
xblPercent = (totalUsersXBL / totalUsers) * 100
psnPercent = (totalUsersPSN / totalUsers) * 100
print(f"pcPercent {pcPercent}")
print(f"xblPercent {xblPercent}")
print(f"psnPercent {psnPercent}")
platData = [xblPercent,psnPercent,pcPercent]
plt.bar(["XBL","PSN","PC"],platData)
plt.title("Playerbase Platform %")
plt.show()