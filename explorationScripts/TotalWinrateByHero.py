import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time


theMap = {
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



file = open("updatedUserStats05-15-1.json","r")
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
            # print(json.dumps(first,indent=4))
            # print(json.dumps(last,indent=4))
            mode = "Elimination"
            modeDiff = (last["modes"][mode]["wins"] - first["modes"][mode]["wins"]) + (last["modes"][mode]["losses"] - first["modes"]["Dominion"]["losses"])
            # totalDiff = (last["wins"] - first["wins"]) + (last["losses"] - first["losses"])
            # total = last["wins"] + last["losses"]
            # if modeDiff > totalDiff * 0.5:
            if True:
                totalUsers += 1
                for hero in first["heros"]:

                    winsDif   = last["heros"][hero]["wins"]   - first["heros"][hero]["wins"]
                    lossesDif = last["heros"][hero]["losses"] - first["heros"][hero]["losses"]
                    totalMatches += winsDif + lossesDif                      
                    theMap[hero]["wins"] += winsDif
                    theMap[hero]["losses"] += lossesDif
                    # # winsDif   = last["heros"][hero]["wins"]  
                    # # lossesDif = last["heros"][hero]["losses"] 
                    
                    # if(winsDif != 0 and lossesDif != 0 and winsDif + lossesDif > 30 and last["heros"][hero]["time"] > 20000):  
                    #     totalMatches += winsDif + lossesDif                      
                    #     theMap[hero].append(winsDif/(winsDif + lossesDif))
print("n = " + str(totalMatches))
print("number of players = " + str(totalUsers))
print("winrate")
winrateList = []
for hero in theMap:
    # winRate = (np.median(theMap[hero])) * 100
    winRate = (theMap[hero]["wins"] / (theMap[hero]["wins"] + theMap[hero]["losses"])) * 100
    winrateList.append((hero,winRate, (theMap[hero]["wins"] + theMap[hero]["losses"])))
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
for hero in winrateList:
    pickrates.append((hero[2] / totalMatches) * 100)

y_pos = np.arange(len(names))


ax.barh(y_pos, winrates, align='center')

for i, v in enumerate(winrates):
    b = float(v)
    ax.text(v + 0.1, i + 0.25, f"{b:.2f}%",
            color = 'black', fontweight = 'bold')

ax.barh(y_pos, pickrates, align='center')

for i, v in enumerate(pickrates):
    b = float(v)
    ax.text(v + 0.1, i + 0.25, f"{b:.2f}%",
            color = 'white', fontweight = 'bold')

ax.set_yticks(y_pos)
ax.set_yticklabels(names)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Winrate / Pickrate (%)')
ax.set_xlim(xmin=0)
ax.set_xlim(xmax=65)
ax.set_title('What is The Winrate and Pickrate by Hero')

ticks = list(range(0,10)) + list(range(50,70))

plt.xticks(ticks,[str(i) for i in ticks])
plt.show()