import json
import datetime
import time
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import CommonDataAnalysisLib as clib


conn = sqlite3.connect("FH.db")
crsr = conn.cursor()

heatDeathOfTheUniverse = 9999999999

# seasonStartDate = 1655395200
seasonStartDate = 1658966400 # Medjay
postSeasonStartDate = 1663248434 # dodge
seasonStartDate = 1663248434 # dodge
postSeasonStartDate = 1666137644 # crossplay phase 2
# postSeasonStartDate = 1666656044 # kensei hitstun+matchmaking

def getHeroWinrateAverages(activeUsers):
    avgPlayerWinrates = {
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

    totalWinrates = {
    "Aramusha" :    {"wins": 0, "losses": 0},
    "Berserker" :   {"wins": 0, "losses": 0},
    "Black Prior" : {"wins": 0, "losses": 0},
    "Centurion" :   {"wins": 0, "losses": 0},
    "Conqueror" :   {"wins": 0, "losses": 0},
    "Gladiator" :   {"wins": 0, "losses": 0},
    "Gryphon" :     {"wins": 0, "losses": 0},
    "Highlander" :  {"wins": 0, "losses": 0},
    "Hitokiri" :    {"wins": 0, "losses": 0},
    "Jiang Jun" :   {"wins": 0, "losses": 0},
    "Jormungandr" : {"wins": 0, "losses": 0},
    "Kensei" :      {"wins": 0, "losses": 0},
    "Kyoshin" :     {"wins": 0, "losses": 0},
    "Lawbringer" :  {"wins": 0, "losses": 0},
    "Medjay" :      {"wins": 0, "losses": 0},
    "Nobushi" :     {"wins": 0, "losses": 0},
    "Nuxia" :       {"wins": 0, "losses": 0},
    "Orochi" :      {"wins": 0, "losses": 0},
    "Peacekeeper" : {"wins": 0, "losses": 0},
    "Pirate" :      {"wins": 0, "losses": 0},
    "Raider" :      {"wins": 0, "losses": 0},
    "Shaman" :      {"wins": 0, "losses": 0},
    "Shaolin" :     {"wins": 0, "losses": 0},
    "Shinobi" :     {"wins": 0, "losses": 0},
    "Shugoki" :     {"wins": 0, "losses": 0},
    "Tiandi" :      {"wins": 0, "losses": 0},
    "Valkyrie" :    {"wins": 0, "losses": 0},
    "Warden" :      {"wins": 0, "losses": 0},
    "Warlord" :     {"wins": 0, "losses": 0},
    "Warmonger" :   {"wins": 0, "losses": 0},
    "Zhanhu" :      {"wins": 0, "losses": 0}
    }

    totalMatches = 0
    includedUserCount = 0
    for user in activeUsers:
        for platform in activeUsers[user]:
            if activeUsers[user][platform][1] != 0:
                stats = activeUsers[user][platform]
                newlist = sorted(stats, key=lambda d: d['time'])
                first = newlist[0]
                last = newlist[-1]

                for hero in first["heros"]:
                    try:
                        x = last["heros"][hero]["wins"] 
                        y = first["heros"][hero]["wins"]
                        winsDif   = last["heros"][hero]["wins"]   - first["heros"][hero]["wins"]
                        lossesDif = last["heros"][hero]["losses"] - first["heros"][hero]["losses"]
                        totalMatches += winsDif + lossesDif                      

                        totalWinrates[hero]["wins"] += winsDif
                        totalWinrates[hero]["losses"] += lossesDif
                        
                        if(winsDif != 0 and lossesDif != 0 and winsDif + lossesDif > 20 and last["heros"][hero]["time"] > 20000):  
                            includedUserCount += 1
                            avgPlayerWinrates[hero].append(winsDif/(winsDif + lossesDif))

                    except Exception as e:
                        ...
                        # print(e)
    
    return {
        "playerAvgsByHero" : avgPlayerWinrates,
        "totalWinrates"    : totalWinrates,
        "includedUserCount": includedUserCount,
        "totalMatches"     : totalMatches
    }

datesToUse = ["NA","28 7 2022","15 9 2022","20 10 2022","3 11 2022","7 12 2022","1 1 2100"]
listOfWinrateData = []

for i in range(len(datesToUse) - 1):
    print(f"getting data from {datesToUse[i]} to {datesToUse[i+1]}")
    seasonStartDate = clib.dateToUnixTime(datesToUse[i])
    seasonEndDate = clib.dateToUnixTime(datesToUse[i+1])
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
        from (SELECT hero.name,hero.wins,hero.losses,hero.timePlayed, stat.username, stat.platform, stat.UTCSeconds 
        FROM hero INNER JOIN stat on hero.playerID = stat.playerID WHERE stat.UTCSeconds BETWEEN {seasonStartDate} AND {seasonEndDate} )
        )
        where UTCSeconds"""
    print("executing SQL")
    crsr.execute(sql)
    ans = crsr.fetchall()
    print("getting active users from data")
    activeUsers = clib.getActiveUsersFromData(SQLData=ans)
    print("getting hero data from user data")
    winrateData = getHeroWinrateAverages(activeUsers=activeUsers)
    listOfWinrateData.append(winrateData)


# file = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\preComputedDatafiles\\winrateOverTime.json",'w')
# file.write(json.dumps(listOfWinrateData))
# file.close()


# a = np.random.normal(size=200)
# b = np.random.normal(size=200)

# fig = plt.figure()
# ax1 = fig.add_subplot(3, 1, 1)
# ax2 = fig.add_subplot(3, 1, 2)
# ax3 = fig.add_subplot(3, 1, 3)

# n, bins, patches = ax1.hist(a)
# ax1.set_xlabel('Angle a (degrees)')
# ax1.set_ylabel('Frequency')

# n, bins, patches = ax2.hist(b)
# ax2.set_xlabel('Angle b (degrees)')
# ax2.set_ylabel('Frequency')

# n, bins, patches = ax3.hist(b)
# ax3.set_xlabel('Angle b (degrees)')
# ax3.set_ylabel('Frequency')

# fig.show()

file = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\preComputedDatafiles\\winrateOverTime.json",'r')
listOfWinrateData = json.load(file)
file.close()

yValuesByHero = {}

for item in listOfWinrateData:
    avgPlayerWinrates = item['playerAvgsByHero']
    for hero in avgPlayerWinrates:
        
        if hero not in yValuesByHero:
            yValuesByHero[hero] = []
        
        yValuesByHero[hero].append(np.mean(avgPlayerWinrates[hero]) * 100)
    
for hero in yValuesByHero:
    yValuesByHero[hero].insert(0,yValuesByHero[hero][0])

subplots = []

file = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\preComputedDatafiles\\winratesbyhero.json",'w')
json.dump(yValuesByHero,file,indent=4)
file.close()

for faction in CommonDataAnalysisLib.factionKey:
    fig, ax = plt.subplots()
    offset = 0
    for hero in CommonDataAnalysisLib.factionKey[faction]:
        y = yValuesByHero[hero]
        x = np.arange(len(y))
        # x = x + offset
        # offset = (offset + 0.025) * - 1
        ax.step(x,y,linewidth=2.5,label=hero)
    ax.set(ylim=(40,70))
    ax.set_xticklabels(datesToUse)
    ax.legend()
    plt.show()

# keys = list(yValuesByHero.keys())
# width = 1
# xInterval = np.arange(len(yValuesByHero[keys[0]]))
# numChartsX = 3
# numChartsY = math.ceil(len(keys) * (1/numChartsX))

# # fig = plt.figure()
# # axes = []

# # iCount = 0
# # for hero in yValuesByHero:
# #     y = yValuesByHero[hero]
# #     iCount += 1
# #     ax = fig.add_subplot(numChartsY,numChartsX,iCount)
# #     # n, bins, patches = ax.bar(yValuesByHero[hero],xInterval)
# #     ax.bar(yValuesByHero[hero],xInterval)
# #     ax.set_xlabel('Update')
# #     ax.set_ylabel('Winrate (%)')

# # plt.show()



# labels = ['G1', 'G2', 'G3', 'G4', 'G5']
# men_means = [20, 34, 30, 35, 27]
# women_means = [25, 32, 34, 20, 25]

# x = np.arange(6)  # the label locations
# width = 0.1  # the width of the bars

# fig, ax = plt.subplots()
# rects1 = ax.bar(x - 2*width, men_means, width, label='Men')
# rects1 = ax.bar(x - width, men_means, width, label='Men')
# rects2 = ax.bar(x  , women_means, width, label='Women')
# rects3 = ax.bar(x + width, women_means, width, label='Women')
# rects3 = ax.bar(x + 2*width, women_means, width, label='Women')

# # Add some text for labels, title and custom x-axis tick labels, etc.
# ax.set_ylabel('Scores')
# ax.set_title('Scores by group and gender')
# # ax.set_xticks(x,labels)
# ax.legend()

# ax.bar_label(rects1, padding=3)
# ax.bar_label(rects2, padding=3)

# fig.tight_layout()

# plt.show()

# for faction in factionKey:
#     plt.rcdefaults()
#     fig, ax = plt.subplots()
#     factionHeros = factionKey[faction]
#     xOffset = 0.0
#     for hero in factionHeros:
#         x = []
#         y = []
#         xTraverse = 0
#         for item in listOfWinrateData:
#             avgPlayerWinrates = item['playerAvgsByHero']
#             totalWinrates = item['totalWinrates']
#             includedUserCount = item['includedUserCount']
#             totalMatches = item['totalMatches']

#             xOffset += 0.0005
#             xTraverse +=1
#             x.append(xTraverse + xOffset)
#             y.append(np.mean(avgPlayerWinrates[hero]) * 100)
#         plt.step(x,y, color=factionHeros[hero],label=hero)
#     plt.xlabel('Date', fontsize=15)
#     plt.ylabel('Winrate (%)', fontsize=15)
#     # plt.ylim(bottom=40, top=70)
#     dateString = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
#     plt.title(f"{faction} Winrate Over Time")
#     plt.legend()
#     # plt.figure(figsize=(50,25))
#     plt.savefig(f"C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\WinrateOverTimeCharts\\{faction}_{dateString}.png")
#     plt.show()
#     plt.close()
    # ax.clear()




# print("n = " + str(totalMatches))
# print("number of players = " + str(includedUserCount))
# print("winrate")
