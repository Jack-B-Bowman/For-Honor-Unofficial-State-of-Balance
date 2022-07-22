import sqlite3
import json
import os
import time
conn = sqlite3.connect("FH.db")
crsr = conn.cursor()
newData = {}
# file = open("updatedUserStats05-18-2.json","r")
# newData = json.load(file)
crsr.execute(f"SELECT MAX(playerID) FROM stat")
lastPlayerID = crsr.fetchall()[0][0]
crsr.execute(f"SELECT MAX(heroID) FROM hero")
lastHeroID = crsr.fetchall()[0][0]
crsr.execute(f"SELECT MAX(modeID) FROM mode")
lastModeID = crsr.fetchall()[0][0]

if lastPlayerID == None:
    lastPlayerID = 0
if lastHeroID == None:
    lastHeroID = 0
if lastModeID == None:
    lastModeID = 0

def mergeJSON(dir,originalFilePath=""):
    directory = dir
    mergedData = ""
    if originalFilePath != "":
        originalFile = open(originalFilePath,"r")
        mergedData = json.load(originalFile)
    else:
        mergedData = {}

    numberOfDupes = 0
    numberOfActive = 0
    count = 0
    for filename in os.listdir(directory):

        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f) and f[-4:] == 'json':
            file = open(f,"r")
            newData = json.load(file)
            for user in newData:
                count += 1

                if(count % 1000 == 0):
                    print(count)

                if user in mergedData:
                    numberOfDupes += 1
                    for platform in newData[user]:
                        platformStatsList = newData[user][platform]
                        for stat in platformStatsList:
                            isNew = True
                            originalStats = mergedData[user][platform]
                            for compareStat in originalStats:
                                if compareStat["time"] == stat["time"]:
                                    isNew = False
                            if isNew:
                                numberOfActive += 1
                                originalStats.append(stat)
                                originalStats = sorted(originalStats,key=lambda d: d['time'])
                                mergedData[user][platform] = originalStats

                else:
                    # count +=1 
                    mergedData[user] = newData[user]
            file.close()
    return mergedData



def insertGlobalStats(stat,lastPlayerID,user):
    if(user == 'b1.exe'):
        print("stop")
    date = stat["date"]
    faction = stat["faction"]
    reputation = stat["reputation"]
    kills = stat["kills"]
    deaths = stat["deaths"]
    assists = stat["assists"]
    wins = stat["wins"]
    losses = stat["losses"]
    time = stat["time"]
    table = "stat"
    statFields = "(playerID,username,platform,faction,UTCSeconds,reputation,kills,deaths,assists,wins,losses,timePlayed)"
    values = f"({lastPlayerID + 1},'{user}','{platform}',{faction},{date},{reputation},{kills},{deaths},{assists},{wins},{losses},{time})"
    sql = (f"INSERT INTO {table} "
            f"{statFields} "
            f"VALUES {values};\n"
    )
    crsr.execute(sql)

def insertModeStats(modeStats, mode, lastPlayerID, lastModeID):
    table = "mode"
    name = mode
    wins = modeStats["wins"]
    losses= modeStats["losses"]
    kills= modeStats["kills"]
    deaths= modeStats["deaths"]
    assists= modeStats["assists"]
    time= modeStats["time"]
    statFields = "(modeID,playerID,name,kills,deaths,assists,wins,losses,timePlayed)"
    values = f"({lastModeID+1},{lastPlayerID+1},'{name}',{kills},{deaths},{assists},{wins},{losses},{time})"
    sql = (f"INSERT INTO {table} "
            f"{statFields} "
            f"VALUES {values};\n"
        )
    crsr.execute(sql)


def insertHeros(heroStats,hero, lastPlayerID, lastHeroID):
        statFields = "(heroID,playerID,name,kills,deaths,assists,wins,losses,timePlayed)"
        values = f"({lastHeroID+1},{lastPlayerID+1},'{hero}',{heroStats['kills']},{heroStats['deaths']},{heroStats['assists']},{heroStats['wins']},{heroStats['losses']},{heroStats['time']})"
        sql = (f"INSERT INTO {table} "
                f"{statFields} "
                f"VALUES {values};\n"
                )
        crsr.execute(sql)

def hasPlayed(user,stat):
    sql = (
        f"SELECT wins, losses, timePlayed, playerID FROM stat WHERE username='{user}' AND platform='{stat['platform']}';"
    )
    crsr.execute(sql)
    ans = crsr.fetchall()
    if len(ans) == 0:
        return True
    maxTup = list(map(max, zip(*ans)))
    wins = maxTup[0]
    losses = maxTup[1]
    playerID = maxTup[3]
    if ans[0] == None:
        return True
    if stat["wins"] > wins or stat["losses"] > losses:
        return True
    crsr.execute(f"""
    UPDATE stat 
    set UTCSeconds = {stat["date"]}
    where playerID = {playerID}
    """)
    return False
print("merging JSON...")
newData = mergeJSON("datafiles")

globalTime = 0
modeTime = 0
heroTime = 0
hasPlayedTime = 0

count = 0
playersUpdated = 0
print("inserting...")
crsr.execute('BEGIN TRANSACTION')
for user in newData:
    # if user == "b1.exe":
    #     print("me")
    count += 1
    if count % 10000 == 0:
        print(f"{count} --> {playersUpdated}")
        # print(f"insertGlobalTime = {(globalTime):.2f}")
        # print(f"insertModeTime = {(modeTime):.2f}")
        # print(f"insertHerolTime = {(heroTime):.2f}")
        # print(f"hasPlayedTime = {(hasPlayedTime):.2f}")
    platforms = newData[user]
    sql = ""
    for platform in platforms:
        if len(platforms[platform]) > 0:
            stats = platforms[platform]
            for stat in stats:
                # start = time.time()
                if(hasPlayed(user,stat)):
                    playersUpdated+=1
                    # end = time.time()
                    # hasPlayedTime += end - start
                    # start = time.time()
                    insertGlobalStats(stat,lastPlayerID,user)
                    # end = time.time()
                    # globalTime += end-start
                    modes = stat["modes"]
                    # start = time.time()
                    for mode in modes:
                        modeStats = modes[mode]
                        insertModeStats(modeStats,mode,lastPlayerID,lastModeID)
                        lastModeID+=1
                    # end = time.time()
                    # modeTime += end-start
                    heros = stat["heros"]
                    # start = time.time()
                    for hero in heros:
                        table = "hero"
                        heroStats=heros[hero]
                        if(heroStats["wins"] > 0 or heroStats["losses"] > 0):
                            insertHeros(heroStats,hero,lastPlayerID,lastHeroID)
                            lastHeroID+=1
                    # end = time.time()
                    # heroTime += end-start
                    lastPlayerID += 1

        



conn.commit()
conn.close()




# for user in newData:
    # get stat from database with username=user and stat@mostRecentDate
    # if stat@wins < user[wins] or stat@losses < user[losses]
        # addUser()
