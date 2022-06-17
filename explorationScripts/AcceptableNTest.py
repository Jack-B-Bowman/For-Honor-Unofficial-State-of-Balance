import matplotlib.pyplot as plt
import numpy as np
import random
import sqlite3
import json
from datetime import datetime
conn = sqlite3.connect("FH.db")
crsr = conn.cursor()

sql = """
    select * from 

    (SELECT 
        maxValues.name, 
        maxValues.username, 
        maxValues.platform, 
        maxValues.heroMatchCount - minValues.heroMatchCount as heroMatchCount, 
        maxValues.totalMatchCount - minValues.totalMatchCount as totalMatchCount, 
        cast(maxValues.overallWins - minValues.overallWins as float) / ((cast(maxValues.overallWins - minValues.overallWins as float)) + (cast(maxValues.overallLosses - minValues.overallLosses as float))) as winrate
        
    FROM

    (SELECT * FROM
    (SELECT name,hero.wins+hero.losses as HeroMatchCount,
    stat.wins+stat.losses as totalMatchCount, 
    stat.wins as overallWins,
    stat.losses as overallLosses, 
    username,platform,UTCSeconds,
    max(UTCSeconds) over (PARTITION by username) as max_date from hero
    INNER JOIN stat
    WHERE hero.playerID=stat.playerID) maxValues
    WHERE UTCSeconds=max_date) maxValues

    INNER JOIN

    (SELECT * FROM
    (SELECT name,hero.wins+hero.losses as HeroMatchCount,
    stat.wins+stat.losses as totalMatchCount, 
    stat.wins as overallWins,
    stat.losses as overallLosses, 
    username,platform,UTCSeconds,
    min(UTCSeconds) over (PARTITION by username) as min_date from hero
    INNER JOIN stat
    WHERE hero.playerID=stat.playerID) minValues
    WHERE UTCSeconds=min_date) minValues

    WHERE maxValues.name=minValues.name and maxValues.username=minValues.username and maxValues.platform=minValues.platform)

    WHERE totalMatchCount > 20 and winrate < 100 and winrate > 0 and heroMatchCount > 0
    """

# crsr.execute(sql)
# ans = crsr.fetchall()

colours = [
    "black",
    "maroon",
    "orangered",
    "gold",
    "darkolivegreen",
    "green",
    "turquoise",
    "dodgerblue",
    "navy",
    "purple"
]

formatStuff = {
    "Samurai": {
        "Aramusha" : colours[0],
        "Hitokiri" : colours[1],
        "Kensei"   : colours[2],
        "Kyoshin"  : colours[3],
        "Nobushi"  : colours[4],
        "Orochi"   : colours[5],
        "Shinobi"  : colours[6],
        "Shugoki"  : colours[7]
    },
    "Knights": {
        "Black Prior" : colours[0],
        "Centurion"   : colours[1],
        "Conqueror"   : colours[2],
        "Gladiator"   : colours[3],
        "Gryphon"     : colours[4],
        "Lawbringer"  : colours[5],
        "Peacekeeper" : colours[6],
        "Warden"      : colours[7],
        "Warmonger"   : colours[8],
    },
    "Vikings": {
        "Berserker"   : colours[0],
        "Highlander"  : colours[1],
        "Jormungandr" : colours[2],
        "Raider"      : colours[3],
        "Shaman"      : colours[4],
        "Valkyrie"    : colours[5],
        "Warlord"     : colours[6],
    },
    "Wu Lin" : {
        "Jiang Jun" : colours[0],
        "Nuxia"     : colours[1],
        "Shaolin"   : colours[2],
        "Tiandi"    : colours[3],
        "Zhanhu"    : colours[4],
    },
    "Outlanders" : {
        "Pirate" : colours[9]
    }
}

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

# for stat in ans:
#     name = stat[0]
#     theMap[name].append(stat[5] * 100)

file = open("AcceptableNTest.json","r")
# file.write(json.dumps(theMap))
theMap = json.load(file)
file.close()

for faction in formatStuff:
    plt.rcdefaults()
    fig, ax = plt.subplots()
    factionHeros = formatStuff[faction]

    base = 2
    exp = 0
    # n = base**exp
    n=1

    for hero in factionHeros:
        
        x = []
        y = []
        while n < len(theMap[hero]):
            avgs = []
            fullList = theMap[hero]
            random.shuffle(fullList)
            for i in range(0,n):
                avg = fullList[i]
                avgs.append(avg)
            y.append(np.mean(avgs))
            x.append(n)

            n += 10
            # exp += 1
            # n = base ** exp
        plt.plot(x,y, color=factionHeros[hero],label=hero)
        n = 1
    ax.set_xscale('log')
    plt.xlabel('N', fontsize=15)
    plt.ylabel('Winrate AVG', fontsize=15)
    dateString = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    plt.title(f"{faction} Winrate N Test")
    plt.legend()
    plt.savefig(f"C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\NTests\\{faction}_{dateString}.png")
    plt.show()
    plt.close()
    ax.clear()

# for hero in theMap:

#     plt.rcdefaults()
#     fig, ax = plt.subplots()
#     x = []
#     y = []
#     for i in range(len(theMap[hero])):
#         if skillBucketsMatchCount[i] > 0:
#             if (i * bucketSize) > 20 and (i * bucketSize) < 90:
#                 x.append(i * bucketSize)
#                 count = skillBucketsMatchCount[i]
#                 heroMatches = theMap[hero][i]
#                 y.append((theMap[hero][i]/skillBucketsMatchCount[i]) * 100)

#     plt.xlabel('Player Winrate (%)', fontsize=15)
#     plt.ylabel('Pickrate (%)', fontsize=15)
#     plt.ylim(bottom=0, top=10)
#     plt.plot(x,y, color="blue",label=hero)
#     averagePSN = np.mean(y)
#     dateString = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
#     plt.title(f"{hero} Pickrate by Skill Bracket")
#     plt.legend()
#     plt.savefig(f"C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\PickrateByWinrateCharts\\{hero}_{dateString}.png")
#     plt.close()
#     ax.clear()

# for i in range(len(skillBucketsMatchCount)):
#     print(f"[{i * bucketSize},{(i + 1) * bucketSize}) : {skillBucketsMatchCount[i]}")
