import json
import datetime

PSNstats = [0,0]
XboxStats = [0,0]
PCstats = [0,0]

file = open("updatedUserStats05-06-2.json","r")
activeUsers = json.load(file)
numUsers = 0
oldestDate = 99999999999999999999999999999999999
for user in activeUsers:
    numUsers += 1
    for platform in activeUsers[user]:
        if len(activeUsers[user][platform]) > 0:
            if activeUsers[user][platform][0]["date"] < oldestDate and activeUsers[user][platform][0]["date"] > 0:
                oldestDate = activeUsers[user][platform][0]["date"]

print(datetime.datetime.fromtimestamp(oldestDate))
print(numUsers)

