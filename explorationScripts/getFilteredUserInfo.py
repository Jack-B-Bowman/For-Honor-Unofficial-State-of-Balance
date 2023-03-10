import CommonDataAnalysisLib as clib
import sqlite3
import json

def parse_heroes(SQLData):
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
        kills = SQLData[i][7]
        deaths = SQLData[i][8]
        assists = SQLData[i][9]

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
                "kills" : kills,
                "deaths" : deaths,
                "assists" : assists,
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
                "kills" : kills,
                "deaths" : deaths,
                "assists" : assists,
                "time" : timePlayed
            }
    print()
    return activeUsers


def parse_modes(SQLData):
    print()
    activeUsers = {}
    counter = 0
    for i in range(len(SQLData)):
        counter += 1
        if counter % 10000 == 0:
            print(f"\rentries parsed: {counter} / {len(SQLData)}",end="")
        mode = SQLData[i][0]
        user = SQLData[i][1]
        date = SQLData[i][2]
        platform = SQLData[i][3]
        wins = SQLData[i][4]
        losses= SQLData[i][5]
        timePlayed = SQLData[i][6]
        kills = SQLData[i][7]
        deaths = SQLData[i][8]
        assists = SQLData[i][9]

        if user not in activeUsers:
            activeUsers[user] = {}
        
        if platform not in activeUsers[user]:
            activeUsers[user][platform] = [0,0]
        
        if activeUsers[user][platform][0] == 0:
            stat = {
                "date" : date,
                "modes": {}
            }

            activeUsers[user][platform][0] = stat


        if activeUsers[user][platform][0]['time'] == date:
            activeUsers[user][platform][0]['modes'][mode]  = {
                "wins" : wins,
                "losses" : losses,
                "kills" : kills,
                "deaths" : deaths,
                "assists" : assists,
                "time" : timePlayed
            }
        
        if activeUsers[user][platform][0]['time'] != date and activeUsers[user][platform][1] == 0:
            stat = {
                "date" : date,
                "modes": {}
            }
            activeUsers[user][platform][1] = stat

        if activeUsers[user][platform][0]['time'] != date:
            activeUsers[user][platform][1]['modes'][mode]  = {
                "wins" : wins,
                "losses" : losses,
                "kills" : kills,
                "deaths" : deaths,
                "assists" : assists,
                "time" : timePlayed
            }
    print()
    return activeUsers


def parse_stats(SQLData):
    print()
    activeUsers = {}
    counter = 0
    for i in range(len(SQLData)):
        counter += 1
        if counter % 10000 == 0:
            print(f"\rentries parsed: {counter} / {len(SQLData)}",end="")
        hero = SQLData[i][0]
        user = SQLData[i][1]
        date = SQLData[i][2]
        platform = SQLData[i][3]
        wins = SQLData[i][4]
        losses= SQLData[i][5]
        timePlayed = SQLData[i][6]
        kills = SQLData[i][7]
        deaths = SQLData[i][8]
        assists = SQLData[i][9]

        if user not in activeUsers:
            activeUsers[user] = {}
        
        if platform not in activeUsers[user]:
            activeUsers[user][platform] = [0,0]
        
        if activeUsers[user][platform][0] == 0:
            stat = {
                "wins" : wins,
                "losses" : losses,
                "kills" : kills,
                "deaths" : deaths,
                "assists" : assists,
                "time_played" : timePlayed,
                "date" : date
            }

            activeUsers[user][platform][0] = stat
        
        if activeUsers[user][platform][0]['date'] != date and activeUsers[user][platform][1] == 0:
            stat = {
                "wins" : wins,
                "losses" : losses,
                "kills" : kills,
                "deaths" : deaths,
                "assists" : assists,
                "time_played" : timePlayed,
                "date" : date
            }
            activeUsers[user][platform][1] = stat
    print()
    return activeUsers

conn = sqlite3.connect("FH.db")
crsr = conn.cursor()

sql_queries = clib.website_sql_queries
dates = clib.UpdateInfo.keys()
epoch_dates = sorted(list(map(clib.dateToUnixTime,dates)))
print(epoch_dates)


crsr.execute(sql_queries["stat_data"](epoch_dates[-2],1676244628))

file = open(r"C:\Users\Jack Bowman\Documents\Programs\PytScripts\UserScraper\website_data\data1.json","w")
json.dump(parse_stats(crsr.fetchall()),file,indent=4)
file.close()