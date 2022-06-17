import json
import matplotlib.pyplot as plt
import numpy as np


file = open("updatedUserStats05-11-5.json","r")
activeUsers = json.load(file)

totalUsers = 0

ratios = []
times = []
for user in activeUsers:
    for platform in activeUsers[user]:
        if len(activeUsers[user][platform]) > 1:
            stats = activeUsers[user][platform]
            newlist = sorted(stats, key=lambda d: d['time'])
            first = newlist[0]
            last = newlist[-1]
            time = last["time"]
            rep  = last["reputation"]
            if rep > 0:
                totalUsers += 1
                timePerRep = time / rep
                ratios.append(timePerRep)
                times.append(time)
mean = np.mean(ratios)
print(f"the mean time per reputation is {((mean / 60)/ 60):.2f} hrs")
mean = np.mean(times)
print(f"the mean time played is         {((mean / 60)/ 60):.2f} hrs")
print("n = " + str(totalUsers))