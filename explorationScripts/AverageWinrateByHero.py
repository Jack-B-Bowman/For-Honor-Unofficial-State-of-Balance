import json
import csv
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
conn = sqlite3.connect("FH.db")
crsr = conn.cursor()

# seasonStartDate = 1655395200 # true season start
seasonStartDate = 1656547619 # post conq nerf 
# seasonStartDate = 1658970014
seasonStartDate = 1658966400 # Medjay
seasonStartDate = 1663248434 # dodge
seasonStartDate = 1666137644 # crossplay phase 2
seasonStartDate = 1666656044 # kensei hitstun+matchmaking

brokenPlayers = []

sql = f"""
select name,
       username,
       UTCSeconds,
       platform,
       wins,
       losses,
	   timePlayed
from (
  select name, 
         username, 
         UTCSeconds,
         max(UTCSeconds) over (partition by username) as max_date,
         min(UTCSeconds) over (partition by username) as min_date,
         platform,
         wins,
         losses,
		 timePlayed
  from (SELECT hero.name,hero.wins,hero.losses,hero.timePlayed, stat.username, stat.platform, stat.UTCSeconds FROM hero INNER JOIN stat on hero.playerID = stat.playerID WHERE stat.UTCSeconds > {seasonStartDate} )
)
where UTCSeconds = max_date OR UTCSeconds = min_date;
"""
crsr.execute(sql)
ans = crsr.fetchall()

activeUsers = {}
counter = 0
lastTime = ans[0][2]
for i in range(len(ans)):
    counter += 1
    if counter % 10000 == 0:
        print(f"\rentries parsed: {counter} / {len(ans)}",end="")
    hero = ans[i][0]
    user = ans[i][1]
    time = ans[i][2]
    platform = ans[i][3]
    wins = ans[i][4]
    losses = ans[i][5]
    timePlayed = ans[i][6]
    # if user == "b1.exe":
    #     print("me")

    # has the user been added yet
    if user in activeUsers:
        currentUser = activeUsers[user]
        # has the user's chosen platform bee added yet
        if platform in activeUsers[user]:
            # should the current hero stat be added to the last stat or a new one
            if time == activeUsers[user][platform][-1]["time"]:
                # is the current stat the first
                if len(activeUsers[user][platform]) == 1:
                    activeUsers[user][platform][-1]["heros"][hero] = {
                        "wins" : wins,
                        "losses" : losses,
                        "time" : timePlayed
                    }
                # the current stat is the last stat and we need to check if the hero exists in the first stat
                else:
                    if hero in activeUsers[user][platform][-2]["heros"]:
                        activeUsers[user][platform][-1]["heros"][hero] = {
                            "wins" : wins,
                            "losses" : losses,
                            "time" : timePlayed
                        }
            else:
                if len(activeUsers[user][platform]) == 1:
                    stat = {
                        "time" : time,
                        "heros": {}
                    }
                    if hero in activeUsers[user][platform][-1]["heros"]:
                        stat["heros"][hero] = {
                            "wins" : wins,
                            "losses" : losses,
                            "time" : timePlayed
                        }
                    activeUsers[user][platform].append(stat)
                else:
                    stat = {
                        "time" : time,
                        "heros": {}
                    }
                    activeUsers[user][platform].append(stat)
        else:
            stat = {
                "time" : time,
                "heros": {}
            }
            stat["heros"][hero] = {
                    "wins" : wins,
                    "losses" : losses,
                    "time" : timePlayed
            }
            activeUsers[user][platform] = [stat]
    else:
        activeUsers[user] = {}
        stat = {
            "time" : time,
            "heros": {}
        }

        stat["heros"][hero] = {
            "wins" : wins,
            "losses" : losses,
            "time" : timePlayed
        }
        activeUsers[user][platform] = [stat]

print()

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
"Zhanhu" : [],
"Medjay" : []
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
"Zhanhu" : {"wins": 0, "losses": 0},
"Medjay" : {"wins": 0, "losses": 0}
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



# file = open("updatedUserStats05-18-2.json","r")
# activeUsers = json.load(file)

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
            # totalDiff = (last["wins"] - first["wins"]) + (last["losses"] - first["losses"])
            # total = last["wins"] + last["losses"]
            # if modeDiff > totalDiff * 0.5:
            if True:
                for hero in first["heros"]:
                    if hero in last["heros"]:
                        x = last["heros"][hero]["wins"] 
                        y = first["heros"][hero]["wins"]
                        winsDif   = last["heros"][hero]["wins"]   - first["heros"][hero]["wins"]
                        lossesDif = last["heros"][hero]["losses"] - first["heros"][hero]["losses"]
                        totalMatches += winsDif + lossesDif                      

                        theMap2[hero]["wins"] += winsDif
                        theMap2[hero]["losses"] += lossesDif
                        
                        if(winsDif != 0 and lossesDif != 0 and winsDif + lossesDif > 20 and last["heros"][hero]["time"] > 20000):  
                            totalUsers += 1
                            theMap[hero].append(winsDif/(winsDif + lossesDif))
                    else:
                        brokenPlayers.append(f"{user},{platform},{hero}\n")
print("n = " + str(totalMatches))
print("number of players = " + str(totalUsers))
print("winrate")
winrateList = []
for hero in theMap:
    winRate = (np.mean(theMap[hero])) * 100
    # winRate = (theMap2[hero]["wins"] / (theMap2[hero]["wins"] + theMap2[hero]["losses"])) * 100
    winrateList.append((hero,winRate, (theMap2[hero]["wins"] + theMap2[hero]["losses"])))
    # winrateList.append((hero,winRate,len(theMap[hero])))
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
    pickrates.append(((theMap2[hero]["wins"] + theMap2[hero]["losses"]) / totalMatches) * 100)

y_pos = np.arange(len(names))

# winrateMean = np.mean(winrates)
# meanDiff = winrateMean - 50
# winrates = list(map(lambda x: x - meanDiff, winrates))

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

ticks = list(range(0,10)) + list(range(30,70))

# print(f"average winrate is off by {meanDiff}%")

plt.xticks(ticks,[str(i) for i in ticks])
plt.show()

file = open("brokenUsers.csv","w")
file.writelines(brokenPlayers)
file.close()


