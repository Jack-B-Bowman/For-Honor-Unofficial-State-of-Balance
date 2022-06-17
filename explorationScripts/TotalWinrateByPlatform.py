import json
import matplotlib.pyplot as plt
import numpy as np

PSNstats = [0,0]
XboxStats = [0,0]
PCstats = [0,0]

file = open("updatedUserStats05-05-1.json","r")
activeUsers = json.load(file)

totalMatches = 0
totalUsers = 0
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


            if last["platform"] == "psn":
                PSNstats[0] += wins
                PSNstats[1] += losses

            if last["platform"] == "xbl":
                XboxStats[0] += wins
                XboxStats[1] += losses

            if last["platform"] == "uplay":
                PCstats[0] += wins
                PCstats[1] += losses


averagePSN =  (PSNstats[0] / (PSNstats[1] + PSNstats[0])) * 100
averageXBOX = (XboxStats[0] / (XboxStats[1] + XboxStats[0])) * 100
averagePC   = (PCstats[0] / (PCstats[1] + PCstats[0])) * 100

print(f"PSN:  {averagePSN:.2f}%\nXBOX: {averageXBOX:.2f}% \nPC:   {averagePC:.2f}%")

