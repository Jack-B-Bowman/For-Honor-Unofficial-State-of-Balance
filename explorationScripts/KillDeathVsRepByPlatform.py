import json
import matplotlib.pyplot as plt
import numpy as np

PSNstats = []
XboxStats = []
PCstats = []

file = open("updatedUserStats05-06-2.json","r")
activeUsers = json.load(file)

totalKDsPC = 0
totalUsersPC = 0
totalKDsPSN = 0
totalUsersPSN = 0
totalKDsXBL = 0
totalUsersXBL = 0

numOver1 = {"xbl" : 0,
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

            kills = (last["kills"] - first["kills"])
            deaths = last["deaths"] - first["deaths"]

            # kills = (last["kills"] - first["kills"]) + (last["assists"] - first["assists"])
            # deaths = last["deaths"] - first["deaths"]
            
            # wins = last["wins"]
            # losses = last["losses"]
            if kills + deaths > 50 and last["reputation"] < 1000: 

                KDRatio = (kills/deaths)

                if KDRatio >= 1:
                    numOver1[platform] += 1

                if(KDRatio < 101):
                    userTuple = (last["reputation"],KDRatio)

                    if last["platform"] == "psn":
                        PSNstats.append(userTuple)
                        totalUsersPSN += 1
                        totalKDsPSN += kills + deaths
                    if last["platform"] == "xbl":
                        XboxStats.append(userTuple)
                        totalUsersXBL += 1
                        totalKDsXBL += kills + deaths
                    if last["platform"] == "uplay":
                        PCstats.append(userTuple)
                        totalUsersPC += 1
                        totalKDsPC += kills + deaths



plt.rcdefaults()
fig, ax = plt.subplots(2, 1, sharex=True)


psnX = [i[0] for i in PSNstats]
psnY = [i[1] for i in PSNstats]

z = np.polyfit(psnX, psnY, 1)
p = np.poly1d(z)
plt.plot(psnX, p(psnX), color="blue")
plt.xlabel('player reputation', fontsize=20)
plt.ylabel('KD Ratio', fontsize=20)
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

print(f"PSN:  {averagePSN:.2f}\t n = {totalUsersPSN} @ {totalKDsPSN}\nXBOX: {averageXBOX:.2f}\t n = {totalUsersXBL} @ {totalKDsXBL} \nPC:   {averagePC:.2f}\t n = {totalUsersPC} @ {totalKDsPC}")

print(f"fraction of players with KD >= 1.0")
print(f"xbox:\t {(numOver1['xbl'] / totalUsersXBL):.2f}")
print(f"psn:\t {(numOver1['psn'] / totalUsersPSN):.2f}")
print(f"pc:\t {(numOver1['uplay'] / totalUsersPC):.2f}")

# print("total matches: " + str(totalMatches))
# print("total players: " + str(totalUsers))

plt.legend()
# plt.plot(playerReps, p(playerReps))
plt.show()

