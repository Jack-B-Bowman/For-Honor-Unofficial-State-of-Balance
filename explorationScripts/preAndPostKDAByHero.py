import json
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
conn = sqlite3.connect("FH.db")
crsr = conn.cursor()

# seasonStartDate = 1655395200
seasonStartDate = 1658966400 # Medjay
postSeasonStartDate = 1663248434 # dodge
seasonStartDate = 1663248434 # dodge
# postSeasonStartDate = 1666137644 # crossplay phase 2
# postSeasonStartDate = 1666656044 # kensei hitstun+matchmaking
# seasonStartDate = 1666137644 # crossplay phase 2
seasonStartDate = 1670392861 # valk & tiandi
postSeasonStartDate = 1675317661 # Afeera

sqlPostSeason = f"""
select name,
       username,
       UTCSeconds,
       platform,
       kills,
       deaths,
       assists,
	   timePlayed
from (
  select name, 
         username, 
         UTCSeconds,
         max(UTCSeconds) over (partition by username) as max_date,
         min(UTCSeconds) over (partition by username) as min_date,
         platform,
         kills,
         deaths,
         assists,
		 timePlayed
  from (SELECT hero.name,hero.kills,hero.deaths,hero.assists,hero.timePlayed, stat.username, stat.platform, stat.UTCSeconds FROM hero INNER JOIN stat on hero.playerID = stat.playerID WHERE stat.UTCSeconds > {postSeasonStartDate} )
)
where UTCSeconds = max_date OR UTCSeconds = min_date;
"""
sqlPreSeason = f"""
select name,
       username,
       UTCSeconds,
       platform,
       kills,
       deaths,
       assists,
	   timePlayed
from (
  select name, 
         username, 
         UTCSeconds,
         max(UTCSeconds) over (partition by username) as max_date,
         min(UTCSeconds) over (partition by username) as min_date,
         platform,
         kills,
         deaths,
         assists,
		 timePlayed
  from (SELECT hero.name,hero.kills,hero.deaths,hero.assists,hero.timePlayed, stat.username, stat.platform, stat.UTCSeconds FROM hero INNER JOIN stat on hero.playerID = stat.playerID WHERE stat.UTCSeconds BETWEEN {seasonStartDate} AND {postSeasonStartDate} )
)
where UTCSeconds = max_date OR UTCSeconds = min_date;
"""
crsr.execute(sqlPreSeason)
ans = crsr.fetchall()

activeUsers = {}
counter = 0
lastTime = ans[0][2]
for i in range(len(ans)):
    counter += 1
    if counter % 10000 == 0:
        print(f"entries parsed: {counter} / {len(ans)}")
    hero = ans[i][0]
    user = ans[i][1]
    time = ans[i][2]
    platform = ans[i][3]
    kills = ans[i][4]
    deaths = ans[i][5]
    assists = ans[i][6]
    timePlayed = ans[i][7]
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
                        "kills" : kills,
                        "deaths" : deaths,
                        "assists": assists,
                        "time" : timePlayed
                    }
                # the current stat is the last stat and we need to check if the hero exists in the first stat
                else:
                    if hero in activeUsers[user][platform][-2]["heros"]:
                        activeUsers[user][platform][-1]["heros"][hero] = {
                            "kills" : kills,
                            "deaths" : deaths,
                            "assists": assists,
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
                            "kills" : kills,
                            "deaths" : deaths,
                            "assists": assists,
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
                "kills" : kills,
                "deaths" : deaths,
                "assists": assists,
                "time" : timePlayed
            }
            activeUsers[user][platform] = [stat]
    # add new user to active users
    else:
        activeUsers[user] = {}
        stat = {
            "time" : time,
            "heros": {}
        }

        stat["heros"][hero] = {
            "kills" : kills,
            "deaths" : deaths,
            "assists": assists,
            "time" : timePlayed
        }
        activeUsers[user][platform] = [stat]



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
"Medjay" : [],
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
"Aramusha" : {"kills": 0, "deaths": 0, "assists": 0},
"Berserker" : {"kills": 0, "deaths": 0, "assists": 0},
"Black Prior" : {"kills": 0, "deaths": 0, "assists": 0},
"Centurion" : {"kills": 0, "deaths": 0, "assists": 0},
"Conqueror" : {"kills": 0, "deaths": 0, "assists": 0},
"Gladiator" : {"kills": 0, "deaths": 0, "assists": 0},
"Gryphon" : {"kills": 0, "deaths": 0, "assists": 0},
"Highlander" : {"kills": 0, "deaths": 0, "assists": 0},
"Hitokiri" : {"kills": 0, "deaths": 0, "assists": 0},
"Jiang Jun" : {"kills": 0, "deaths": 0, "assists": 0},
"Jormungandr" : {"kills": 0, "deaths": 0, "assists": 0},
"Kensei" : {"kills": 0, "deaths": 0, "assists": 0},
"Kyoshin" : {"kills": 0, "deaths": 0, "assists": 0},
"Lawbringer" : {"kills": 0, "deaths": 0, "assists": 0},
"Medjay" : {"kills": 0, "deaths": 0, "assists": 0},
"Nobushi" : {"kills": 0, "deaths": 0, "assists": 0},
"Nuxia" : {"kills": 0, "deaths": 0, "assists": 0},
"Orochi" : {"kills": 0, "deaths": 0, "assists": 0},
"Peacekeeper" : {"kills": 0, "deaths": 0, "assists": 0},
"Pirate" : {"kills": 0, "deaths": 0, "assists": 0},
"Raider" : {"kills": 0, "deaths": 0, "assists": 0},
"Shaman" : {"kills": 0, "deaths": 0, "assists": 0},
"Shaolin" : {"kills": 0, "deaths": 0, "assists": 0},
"Shinobi" : {"kills": 0, "deaths": 0, "assists": 0},
"Shugoki" : {"kills": 0, "deaths": 0, "assists": 0},
"Tiandi" : {"kills": 0, "deaths": 0, "assists": 0},
"Valkyrie" : {"kills": 0, "deaths": 0, "assists": 0},
"Warden" : {"kills": 0, "deaths": 0, "assists": 0},
"Warlord" : {"kills": 0, "deaths": 0, "assists": 0},
"Warmonger" : {"kills": 0, "deaths": 0, "assists": 0},
"Zhanhu" : {"kills": 0, "deaths": 0, "assists": 0}
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

totalKD = 0
totalUsers = 0
for user in activeUsers:
    for platform in activeUsers[user]:
        if len(activeUsers[user][platform]) > 1:
            stats = activeUsers[user][platform]
            newlist = sorted(stats, key=lambda d: d['time'])
            first = newlist[0]
            last = newlist[-1]

            if True:
                for hero in first["heros"]:
                    try:

                        killsDif    = last["heros"][hero]["kills"]   - first["heros"][hero]["kills"]
                        deathsDif  = last["heros"][hero]["deaths"] - first["heros"][hero]["deaths"]
                        assistsDif = last["heros"][hero]["assists"] - first["heros"][hero]["assists"]

                        totalKD += killsDif + deathsDif                      

                        theMap2[hero]["kills"] += killsDif
                        theMap2[hero]["deaths"] += deathsDif
                        theMap2[hero]["assists"] += assistsDif
                        
                        if(killsDif != 0 and deathsDif != 0 and killsDif + deathsDif > 20 and last["heros"][hero]["time"] > 20000):  
                            totalUsers += 1
                            theMap[hero].append((killsDif + assistsDif) / deathsDif)

                    except Exception as e:
                        print(e)
print("n = " + str(totalKD))
print("number of players = " + str(totalUsers))
print("kdarate")
KDARateList = []
for hero in theMap:
    KDARate = (np.mean(theMap[hero]))
    KDARateList.append((hero,KDARate, (theMap2[hero]["kills"] + theMap2[hero]["deaths"] + theMap2[hero]["assists"])))

KDARateList.sort(key=lambda y:y[1])
KDARateList.reverse()
for hero in KDARateList:
    print(f"{hero[0]}   :\t {hero[1]:.2f}% \t n = {hero[2]}" )


plt.rcdefaults()
fig, ax = plt.subplots()


names = [i[0] for i in KDARateList]
KDARatios = [i[1] for i in KDARateList]


y_pos = np.arange(len(names))



ax.barh(y_pos, KDARatios, align='center')

for i, v in enumerate(KDARatios):
    b = float(v)
    ax.text(v + 0.1, i + 0.25, f"{b:.2f}%",
            color = 'black', fontweight = 'bold')

ax.set_yticks(y_pos)
ax.set_yticklabels(names)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('KDA Ratio')
ax.set_xlim(xmin=0)
ax.set_xlim(xmax=65)
ax.set_title('What is The KDA Ratio by Hero')

ticks = list(range(0,10)) + list(range(30,70))


data = {}
for i in range(len(KDARatios)):
    name = names[i]
    data[name] = KDARatios[i]

file = open("preComputedDatafiles\\preSeasonDataKDA.json","w")
file.write(json.dumps(data,indent=4))
file.close()
plt.xticks(ticks,[str(i) for i in ticks])
plt.show()