import datetime
import time


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

factionKey = {
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
        "Pirate" : colours[9],
        "Medjay" : colours[8],
    }
}

UpdateInfo = {
    "7 12 2022" : {
        "version" : "2.40.0",
        "patchnotes" : "https://www.ubisoft.com/en-gb/game/for-honor/news-updates/5K7gJrsS7BGjegCjnnZydv/patch-notes-2400-for-honor",
        "notes" : "valk+tiandi rework"
    },

    "3 11 2022" : {
        "version" : "2.39.2",
        "patchnotes" : "https://www.ubisoft.com/en-gb/game/for-honor/news-updates/2hBzypk8Z7LnGX3r2pP64n/patch-notes-2392-for-honor",
        "notes"  : "bugfix"
    },
    "25 10 2022" : {
        "version" : "2.39.1",
        "patchnotes" : "https://www.ubisoft.com/en-gb/game/for-honor/news-updates/2U2b9JmaL4m0eAMUy4buFN/patch-notes-2391-for-honor",
        "notes"  : "Kensei Hitstun"
    },
    "20 10 2022" : {
        "version" : "2.39.0",
        "patchnotes" : "https://www.ubisoft.com/en-gb/game/for-honor/news-updates/2203fmh7jD1gohfN25aDRi/patch-notes-2390-for-honor",
        "notes" : "crossplay phase 2"
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