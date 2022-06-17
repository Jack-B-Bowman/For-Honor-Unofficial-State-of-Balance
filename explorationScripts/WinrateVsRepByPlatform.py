import json
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
conn = sqlite3.connect("FH.db")
crsr = conn.cursor()

crsr.execute("""select 
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
where UTCSeconds = max_date OR UTCSeconds = min_date;""")

ans = crsr.fetchall()

activeUsers = {}

for i in range(len(ans)):
    user = ans[i][0]
    platform = ans[i][1]
    time = ans[i][2]
    wins = ans[i][3]
    losses = ans[i][4]
    reputation = ans[i][5]
    if user in activeUsers:
        if platform in activeUsers[user]:
            stat = {
                "time" : time,
                "wins" : wins,
                "losses" : losses,
                "reputation" : reputation,
                "platform" : platform
            }          
            activeUsers[user][platform].append(stat)
        else:
            stat = {
                "time" : time,
                "wins" : wins,
                "losses" : losses,
                "reputation" : reputation
            }          
            activeUsers[user][platform] = [stat]
    else:
        stat = {
            "wins" : wins,
            "losses" : losses,
            "time" : time,
            "reputation" : reputation
        } 
        activeUsers[user] = {}
        activeUsers[user][platform] = [stat]


PSNstats = []
XboxStats = []
PCstats = []

# file = open("updatedUserStats05-06-2.json","r")7
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

for user in activeUsers:
    for platform in activeUsers[user]:
        if len(activeUsers[user][platform]) > 1:
            stats = activeUsers[user][platform]
            newlist = sorted(stats, key=lambda d: d['time'])
            first = newlist[0]
            last = newlist[-1]

            wins = last["wins"] - first["wins"]
            losses = last["losses"] - first["losses"]
            # wins = last["wins"]
            # losses = last["losses"]
            if wins + losses > 20 and last["reputation"] < 600: 

                winRate = (wins/(wins + losses)) * 100

                if winRate >= 50:
                    numOver60[platform] += 1

                if(winRate < 101):
                    userTuple = (last["reputation"],winRate)

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



plt.rcdefaults()
fig, ax = plt.subplots()


psnX = [i[0] for i in PSNstats]
psnY = [i[1] for i in PSNstats]

z = np.polyfit(psnX, psnY, 1)
p = np.poly1d(z)
plt.plot(psnX, p(psnX), color="blue")
plt.xlabel('player reputation', fontsize=20)
plt.ylabel('MMR (winrate)', fontsize=20)
plt.scatter(psnX,psnY, s=0.5, color="blue",label='PSN')
averagePSN = np.mean(psnY)

xblX = [i[0] for i in XboxStats]
xblY = [i[1] for i in XboxStats]

z = np.polyfit(xblX, xblY, 1)
p = np.poly1d(z)
plt.plot(xblX, p(xblX), color="green")
plt.scatter(xblX,xblY, s=0.5, color="green",label="xbox")
averageXBOX = np.mean(xblY)


pcX = [i[0] for i in PCstats]
pcY = [i[1] for i in PCstats]
z = np.polyfit(pcX, pcY, 1)
p = np.poly1d(z)
plt.plot(pcX, p(pcX), color="red")
plt.scatter(pcX,pcY, s=0.5, color="red",label="PC")
averagePC = np.mean(pcY)

print(f"PSN:  {averagePSN:.2f}%\t n = {totalUsersPSN} @ {totalMatchesPSN}\nXBOX: {averageXBOX:.2f}%\t n = {totalUsersXBL} @ {totalMatchesXBL} \nPC:   {averagePC:.2f}%\t n = {totalUsersPC} @ {totalMatchesPC}")

print(f"fraction of players with winrate >= 50%")
print(f"xbox:\t {(numOver60['xbl'] / totalUsersXBL):.2f}")
print(f"psn:\t {(numOver60['psn'] / totalUsersPSN):.2f}")
print(f"pc:\t {(numOver60['uplay'] / totalUsersPC):.2f}")

# print("total matches: " + str(totalMatches))
# print("total players: " + str(totalUsers))

plt.legend()
# plt.plot(playerReps, p(playerReps))
plt.show()

