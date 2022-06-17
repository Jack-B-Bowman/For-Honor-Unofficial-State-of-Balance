import json
import matplotlib.pyplot as plt
import numpy as np

PSNstats = []
XboxStats = []
PCstats = []

file = open("updatedUserStats05-06-2.json","r")
activeUsers = json.load(file)

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

fractions = {
    "psn"   : [0,0,0,0,0,0,0,0,0,0],
    "xbl"   : [0,0,0,0,0,0,0,0,0,0],
    "uplay" : [0,0,0,0,0,0,0,0,0,0]
}

for i in range(0,10):
    lowerFraction = i * 10
    upperFraction = (i+1) * 10

    for player in PSNstats:
        if player[1] >= lowerFraction and player[1] < upperFraction:
            fractions["psn"][i] += 1

    for player in XboxStats:
        if player[1] >= lowerFraction and player[1] < upperFraction:
            fractions["xbl"][i] += 1

    for player in PCstats:
        if player[1] >= lowerFraction and player[1] < upperFraction:
            fractions["uplay"][i] += 1
        

theString = ""

print("player stat fractions")
for i in range(10):
    print(f"{i * 10}% to {(i+1) * 10}%")
    print(f"PSN: {((fractions['psn'][i]  / totalUsersPSN)   * 100):.2f}%")
    print(f"XBL: {((fractions['xbl'][i]  / totalUsersXBL)   * 100):.2f}%")
    print(f"PC : {((fractions['uplay'][i]/ totalUsersPC )   * 100):.2f}%")