import json
import datetime
import time
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
conn = sqlite3.connect("FH.db")
crsr = conn.cursor()

heatDeathOfTheUniverse = 9999999999

# seasonStartDate = 1655395200
seasonStartDate = 1658966400 # Medjay
postSeasonStartDate = 1663248434 # dodge
seasonStartDate = 1663248434 # dodge
postSeasonStartDate = 1666137644 # crossplay phase 2
# postSeasonStartDate = 1666656044 # kensei hitstun+matchmaking

dates = {
    "7 12 2022" : {
        "version" : "2.40.0",
        "patchnotes" : "https://www.ubisoft.com/en-gb/game/for-honor/news-updates/5K7gJrsS7BGjegCjnnZydv/patch-notes-2400-for-honor",
        "notes" : "valk+tiandi rework"
    },

    "3 11 2022" : {
        "version" : "2.39.2",
        "patchnotes" : "https://www.ubisoft.com/en-gb/game/for-honor/news-updates/2hBzypk8Z7LnGX3r2pP64n/patch-notes-2392-for-honor",
    },
    "25 10 2022" : {
        "version" : "2.39.1",
        "patchnotes" : "https://www.ubisoft.com/en-gb/game/for-honor/news-updates/2U2b9JmaL4m0eAMUy4buFN/patch-notes-2391-for-honor",
    },
    "20 10 2022" : {
        "version" : "2.39.0",
        "patchnotes" : "https://www.ubisoft.com/en-gb/game/for-honor/news-updates/2203fmh7jD1gohfN25aDRi/patch-notes-2390-for-honor",
        "notes" : "crosplay phase 2"
    },
    "15 9 2022" : {
        "version" : "2.38.0",
        "patchnotes" : "https://www.ubisoft.com/en-gb/game/for-honor/news-updates/6yK8Z1hgpAoScO2THLLdYD/patch-notes-2380-for-honor",
        "notes" : "dodge attack",
    },
    "28 7 2022" : {
        "version" : "2.37.1",
        "patchnotes" : "https://www.ubisoft.com/en-gb/game/for-honor/news-updates/7Cn4O1wYyV0qXbMOE2gtqI/patch-notes-2371-for-honor",
        "notes" : "Medjay"
    },
    "30 6 2022" : {
        "version" : "2.36.3",
        "patchnotes" : "https://www.ubisoft.com/en-gb/game/for-honor/news-updates/1OBhqnANLD7C5Itm7ObLld/patch-notes-2363-for-honor",
    },
    "27 4 2022" : {
        "version" : "2.35.0",
        "patchnotes" : "https://www.ubisoft.com/en-gb/game/for-honor/news-updates/5Pm3q0Ox2Ed9YRQe3Kuq1m/patch-notes-2351-for-honor",
    },
}

sqlPostSeason = f"""
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
  from (SELECT hero.name,hero.wins,hero.losses,hero.timePlayed, stat.username, stat.platform, stat.UTCSeconds FROM hero INNER JOIN stat on hero.playerID = stat.playerID WHERE stat.UTCSeconds > {postSeasonStartDate} )
)
where UTCSeconds = max_date OR UTCSeconds = min_date;
"""
sqlPreSeason = f"""
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
  from (SELECT hero.name,hero.wins,hero.losses,hero.timePlayed, stat.username, stat.platform, stat.UTCSeconds FROM hero INNER JOIN stat on hero.playerID = stat.playerID WHERE stat.UTCSeconds BETWEEN {seasonStartDate} AND {postSeasonStartDate} )
)
where UTCSeconds = max_date OR UTCSeconds = min_date;
"""


def dateToUnixTime(date):
    dateData = date.split()
    dateTime = datetime.datetime(int(dateData[2]),int(dateData[1]),int(dateData[0]))
    return time.mktime(dateTime.timetuple())



def getActiveUsersFromData(SQLData):
    print()
    activeUsers = {}
    counter = 0
    for i in range(len(SQLData)):
        counter += 1
        if counter % 10000 == 0:
            print(f"\rentries parsed: {counter} / {len(SQLData)}",end="")
        hero = SQLData[i][0]
        user = SQLData[i][1]
        time = SQLData[i][2]
        platform = SQLData[i][3]
        wins = SQLData[i][4]
        losses= SQLData[i][5]
        timePlayed = SQLData[i][6]

        if user not in activeUsers:
            activeUsers[user] = {}
        
        if platform not in activeUsers[user]:
            activeUsers[user][platform] = [0,0]
        
        if activeUsers[user][platform][0] == 0:
            stat = {
                "time" : time,
                "heros": {}
            }

            activeUsers[user][platform][0] = stat


        if activeUsers[user][platform][0]['time'] == time:
            activeUsers[user][platform][0]['heros'][hero]  = {
                "wins" : wins,
                "losses" : losses,
                "time" : timePlayed
            }
        
        if activeUsers[user][platform][0]['time'] != time and activeUsers[user][platform][1] == 0:
            stat = {
                "time" : time,
                "heros": {}
            }
            activeUsers[user][platform][1] = stat

        if activeUsers[user][platform][0]['time'] != time:
            activeUsers[user][platform][1]['heros'][hero]  = {
                "wins" : wins,
                "losses" : losses,
                "time" : timePlayed
            }

                                                        
            



    
    print()
    return activeUsers


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
                        print(e)
    
    return {
        "playerAvgsByHero" : avgPlayerWinrates,
        "totalWinrates"    : totalWinrates,
        "includedUserCount": includedUserCount,
        "totalMatches"     : totalMatches
    }

datesToUse = ["28 7 2022","15 9 2022","20 10 2022","1 1 9999"]
listOfWinrateData = []

crsr.execute(sqlPostSeason)
ans = crsr.fetchall()

activeUsers = getActiveUsersFromData(SQLData=ans)

winrateData = getHeroWinrateAverages(activeUsers=activeUsers)

avgPlayerWinrates = winrateData['playerAvgsByHero']
totalWinrates = winrateData['totalWinrates']
includedUserCount = winrateData['includedUserCount']
totalMatches = winrateData['totalMatches']

print("n = " + str(totalMatches))
print("number of players = " + str(includedUserCount))
print("winrate")
