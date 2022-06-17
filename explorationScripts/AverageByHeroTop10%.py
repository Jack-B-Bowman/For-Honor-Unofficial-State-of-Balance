import json
from turtle import color
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

theMap = {
"Aramusha" : [],
"Berserker" : [],
"Black Prior" : [],
"Centurion" : [],
"Conqueror" : [],
"Gladiator" : [],
"Gryphon" : [],
"Highlander" : [],
"Hitokiri" : [],
"Jiang Jun" : [],
"Jormungandr" : [],
"Kensei" : [],
"Kyoshin" : [],
"Lawbringer" : [],
"Nobushi" : [],
"Nuxia" : [],
"Orochi" : [],
"Peacekeeper" : [],
"Pirate" : [],
"Raider" : [],
"Shaman" : [],
"Shaolin" : [],
"Shinobi" : [],
"Shugoki" : [],
"Tiandi" : [],
"Valkyrie" : [],
"Warden" : [],
"Warlord" : [],
"Warmonger" : [],
"Zhanhu" : []
}

theMap2 = {
"Aramusha" : {"wins": 0, "losses": 0},
"Berserker" : {"wins": 0, "losses": 0},
"Black Prior" : {"wins": 0, "losses": 0},
"Centurion" : {"wins": 0, "losses": 0},
"Conqueror" : {"wins": 0, "losses": 0},
"Gladiator" : {"wins": 0, "losses": 0},
"Gryphon" : {"wins": 0, "losses": 0},
"Highlander" : {"wins": 0, "losses": 0},
"Hitokiri" : {"wins": 0, "losses": 0},
"Jiang Jun" : {"wins": 0, "losses": 0},
"Jormungandr" : {"wins": 0, "losses": 0},
"Kensei" : {"wins": 0, "losses": 0},
"Kyoshin" : {"wins": 0, "losses": 0},
"Lawbringer" : {"wins": 0, "losses": 0},
"Nobushi" : {"wins": 0, "losses": 0},
"Nuxia" : {"wins": 0, "losses": 0},
"Orochi" : {"wins": 0, "losses": 0},
"Peacekeeper" : {"wins": 0, "losses": 0},
"Pirate" : {"wins": 0, "losses": 0},
"Raider" : {"wins": 0, "losses": 0},
"Shaman" : {"wins": 0, "losses": 0},
"Shaolin" : {"wins": 0, "losses": 0},
"Shinobi" : {"wins": 0, "losses": 0},
"Shugoki" : {"wins": 0, "losses": 0},
"Tiandi" : {"wins": 0, "losses": 0},
"Valkyrie" : {"wins": 0, "losses": 0},
"Warden" : {"wins": 0, "losses": 0},
"Warlord" : {"wins": 0, "losses": 0},
"Warmonger" : {"wins": 0, "losses": 0},
"Zhanhu" : {"wins": 0, "losses": 0}
}

# file = open("updatedUserStats04-28-2.json","r")
# data = json.load(file)
# file.close()

# user = "ohh phantoms"

# if user in data:
#     print("exists")

# file = open("mergedUserDataFile5.json","r")
# data = json.load(file)
# file.close()
# activeUsers = {}
# numPlayers = 0
# users = []
# for user in data:
#     numPlayers += 1
#     for platform in data[user]:
#         if len(data[user][platform]) > 0:
#                 username = user.split(" ")
#                 username = "%20".join(username)
#                 users.append((platform,username))

playerWinrates = []

file = open("updatedUserStats05-18-2.json","r")
activeUsers = json.load(file)
top10 = 0
totalMatches = 0
totalUsers = 0

# get the winrates of each user
for user in activeUsers:
    for platform in activeUsers[user]:
        if len(activeUsers[user][platform]) > 1:
            stats = activeUsers[user][platform]
            newlist = sorted(stats, key=lambda d: d['time'])
            first = newlist[0]
            last = newlist[-1]


            # print(json.dumps(first,indent=4))
            # print(json.dumps(last,indent=4))
            # mode = "Elimination"
            # modeDiff = (last["modes"][mode]["wins"] - first["modes"][mode]["wins"]) + (last["modes"][mode]["losses"] - first["modes"]["Dominion"]["losses"])
            totalDiff = (last["wins"] - first["wins"]) + (last["losses"] - first["losses"])
            winsDif   = last["wins"]   - first["wins"]
            lossesDif = last["losses"] - first["losses"]
            if totalDiff >= 30:
                winsDif   = last["wins"]   - first["wins"]
                lossesDif = last["losses"] - first["losses"]
                playerWinrates.append((winsDif/(winsDif + lossesDif)) * 100)

top10 = np.percentile(playerWinrates,90)

for user in activeUsers:
    for platform in activeUsers[user]:
        if len(activeUsers[user][platform]) > 1:
            stats = activeUsers[user][platform]
            newlist = sorted(stats, key=lambda d: d['time'])
            first = newlist[0]
            last = newlist[-1]


            # print(json.dumps(first,indent=4))
            # print(json.dumps(last,indent=4))
            # mode = "Elimination"
            # modeDiff = (last["modes"][mode]["wins"] - first["modes"][mode]["wins"]) + (last["modes"][mode]["losses"] - first["modes"]["Dominion"]["losses"])
            totalDiff = (last["wins"] - first["wins"]) + (last["losses"] - first["losses"])
            total = last["wins"] + last["losses"]
            winsDif   = last["wins"]   - first["wins"]
            lossesDif = last["losses"] - first["losses"]
            if winsDif != 0 and lossesDif != 0:
                # if modeDiff > totalDiff * 0.5:
                if ((winsDif/(winsDif + lossesDif)) * 100) >= top10:
                    for hero in first["heros"]:

                        winsDif   = last["heros"][hero]["wins"]   - first["heros"][hero]["wins"]
                        lossesDif = last["heros"][hero]["losses"] - first["heros"][hero]["losses"]
                        totalMatches += winsDif + lossesDif                      

                        theMap2[hero]["wins"] += winsDif
                        theMap2[hero]["losses"] += lossesDif
                        
                        if(winsDif != 0 and lossesDif != 0 and winsDif + lossesDif > 10 and last["heros"][hero]["time"] > 20000):  
                            totalUsers += 1
                            theMap[hero].append(winsDif/(winsDif + lossesDif))

print("n = " + str(totalMatches))
print("number of players = " + str(totalUsers))
print("winrate")
winrateList = []
for hero in theMap:
    winRate = (np.mean(theMap[hero])) * 100
    winrateList.append((hero,winRate, (theMap2[hero]["wins"] + theMap2[hero]["losses"])))
    # print(f"{hero} : {winRate:.2f}%")

winrateList.sort(key=lambda y:y[1])
winrateList.reverse()
for hero in winrateList:
    print(f"{hero[0]}   :\t {hero[1]:.2f}% \t n = {hero[2]}" )
    # print(f"{hero[0]}" )

# for hero in winrateList:
#     # print(f"{hero[1]}   :\t {hero[0]:.2f}% \t n = {hero[2]}" )
#     print(f"{hero[1]}" )

# for hero in winrateList:
#     # print(f"{hero[1]}   :\t {hero[0]:.2f}% \t n = {hero[2]}" )
#     print(f"{hero[2]}" )

plt.rcdefaults()
fig, ax = plt.subplots()


names = [i[0] for i in winrateList]
winrates = [i[1] for i in winrateList]


pickrates = []
for hero in names:
    pickrates.append((hero,((theMap2[hero]["wins"] + theMap2[hero]["losses"]) / totalMatches) * 100))

pickrates.sort(key=lambda y:y[1])
pickrates.reverse()

names = [i[0] for i in pickrates]
pickrates = [i[1] for i in pickrates]

y_pos = np.arange(len(names))

ax.barh(y_pos, pickrates, align='center',color="#18449a")
nameOrder = names
for i, v in enumerate(pickrates):
    b = float(v)
    ax.text(-1, i + 0.25, f"{b:.2f}%",
            color = 'black', fontweight = 'bold')


theMap = {
"Aramusha" : [],
"Berserker" : [],
"Black Prior" : [],
"Centurion" : [],
"Conqueror" : [],
"Gladiator" : [],
"Gryphon" : [],
"Highlander" : [],
"Hitokiri" : [],
"Jiang Jun" : [],
"Jormungandr" : [],
"Kensei" : [],
"Kyoshin" : [],
"Lawbringer" : [],
"Nobushi" : [],
"Nuxia" : [],
"Orochi" : [],
"Peacekeeper" : [],
"Pirate" : [],
"Raider" : [],
"Shaman" : [],
"Shaolin" : [],
"Shinobi" : [],
"Shugoki" : [],
"Tiandi" : [],
"Valkyrie" : [],
"Warden" : [],
"Warlord" : [],
"Warmonger" : [],
"Zhanhu" : []
}

theMap2 = {
"Aramusha" : {"wins": 0, "losses": 0},
"Berserker" : {"wins": 0, "losses": 0},
"Black Prior" : {"wins": 0, "losses": 0},
"Centurion" : {"wins": 0, "losses": 0},
"Conqueror" : {"wins": 0, "losses": 0},
"Gladiator" : {"wins": 0, "losses": 0},
"Gryphon" : {"wins": 0, "losses": 0},
"Highlander" : {"wins": 0, "losses": 0},
"Hitokiri" : {"wins": 0, "losses": 0},
"Jiang Jun" : {"wins": 0, "losses": 0},
"Jormungandr" : {"wins": 0, "losses": 0},
"Kensei" : {"wins": 0, "losses": 0},
"Kyoshin" : {"wins": 0, "losses": 0},
"Lawbringer" : {"wins": 0, "losses": 0},
"Nobushi" : {"wins": 0, "losses": 0},
"Nuxia" : {"wins": 0, "losses": 0},
"Orochi" : {"wins": 0, "losses": 0},
"Peacekeeper" : {"wins": 0, "losses": 0},
"Pirate" : {"wins": 0, "losses": 0},
"Raider" : {"wins": 0, "losses": 0},
"Shaman" : {"wins": 0, "losses": 0},
"Shaolin" : {"wins": 0, "losses": 0},
"Shinobi" : {"wins": 0, "losses": 0},
"Shugoki" : {"wins": 0, "losses": 0},
"Tiandi" : {"wins": 0, "losses": 0},
"Valkyrie" : {"wins": 0, "losses": 0},
"Warden" : {"wins": 0, "losses": 0},
"Warlord" : {"wins": 0, "losses": 0},
"Warmonger" : {"wins": 0, "losses": 0},
"Zhanhu" : {"wins": 0, "losses": 0}
}


# get the winrates of each user
for user in activeUsers:
    for platform in activeUsers[user]:
        if len(activeUsers[user][platform]) > 1:
            stats = activeUsers[user][platform]
            newlist = sorted(stats, key=lambda d: d['time'])
            first = newlist[0]
            last = newlist[-1]


            # print(json.dumps(first,indent=4))
            # print(json.dumps(last,indent=4))
            # mode = "Elimination"
            # modeDiff = (last["modes"][mode]["wins"] - first["modes"][mode]["wins"]) + (last["modes"][mode]["losses"] - first["modes"]["Dominion"]["losses"])
            totalDiff = (last["wins"] - first["wins"]) + (last["losses"] - first["losses"])
            winsDif   = last["wins"]   - first["wins"]
            lossesDif = last["losses"] - first["losses"]
            if totalDiff >= 30:
                winsDif   = last["wins"]   - first["wins"]
                lossesDif = last["losses"] - first["losses"]
                playerWinrates.append((winsDif/(winsDif + lossesDif)) * 100)

top10 = np.percentile(playerWinrates,90)





for user in activeUsers:
    for platform in activeUsers[user]:
        if len(activeUsers[user][platform]) > 1:
            stats = activeUsers[user][platform]
            newlist = sorted(stats, key=lambda d: d['time'])
            first = newlist[0]
            last = newlist[-1]


            # print(json.dumps(first,indent=4))
            # print(json.dumps(last,indent=4))
            # mode = "Elimination"
            # modeDiff = (last["modes"][mode]["wins"] - first["modes"][mode]["wins"]) + (last["modes"][mode]["losses"] - first["modes"]["Dominion"]["losses"])
            totalDiff = (last["wins"] - first["wins"]) + (last["losses"] - first["losses"])
            total = last["wins"] + last["losses"]
            winsDif   = last["wins"]   - first["wins"]
            lossesDif = last["losses"] - first["losses"]
            if winsDif != 0 and lossesDif != 0:
                # if modeDiff > totalDiff * 0.5:
                if ((winsDif/(winsDif + lossesDif)) * 100) >= 0:
                    for hero in first["heros"]:

                        winsDif   = last["heros"][hero]["wins"]   - first["heros"][hero]["wins"]
                        lossesDif = last["heros"][hero]["losses"] - first["heros"][hero]["losses"]
                        totalMatches += winsDif + lossesDif                      

                        theMap2[hero]["wins"] += winsDif
                        theMap2[hero]["losses"] += lossesDif
                        
                        if(winsDif != 0 and lossesDif != 0 and winsDif + lossesDif > 10 and last["heros"][hero]["time"] > 20000):  
                            totalUsers += 1
                            theMap[hero].append(winsDif/(winsDif + lossesDif))

print("n = " + str(totalMatches))
print("number of players = " + str(totalUsers))
print("winrate")
winrateList = []
for hero in theMap:
    winRate = (np.mean(theMap[hero])) * 100
    winrateList.append((hero,winRate, (theMap2[hero]["wins"] + theMap2[hero]["losses"])))
    # print(f"{hero} : {winRate:.2f}%")

winrateList.sort(key=lambda y:y[1])
winrateList.reverse()
for hero in winrateList:
    print(f"{hero[0]}   :\t {hero[1]:.2f}% \t n = {hero[2]}" )
    # print(f"{hero[0]}" )



# names = [i[0] for i in winrateList]
winrates = [i[1] for i in winrateList]

pickrates = []
for hero in nameOrder:
    pickrates.append((hero,((theMap2[hero]["wins"] + theMap2[hero]["losses"]) / totalMatches) * 100))

# pickrates.sort(key=lambda y:y[1])
# pickrates.reverse()

# names = [i[0] for i in pickrates]
pickrates = [i[1] for i in pickrates]

# y_pos = np.arange(len(names))

ax.barh(y_pos, pickrates, align='center',color="#996E18",height=0.3) 

# for i, v in enumerate(pickrates):
#     b = float(v)
#     ax.text(v - 5.0, i + 0.25, f"{b:.2f}%",
#             color = 'black', fontweight = 'bold')


ax.set_yticks(y_pos)
ax.set_yticklabels(names)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Pickrate (%)')
ax.set_xlim(xmin=0)
ax.set_xlim(xmax=10)
ax.set_title('What is the Overall Pickrate of Heros')

ticks = list(range(0,10))

plt.xticks(ticks,[str(i) for i in ticks])
plt.show()