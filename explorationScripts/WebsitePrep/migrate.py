import sqlite3
import json
import pymongo
import os
import convert_datadump_to_json as dd
from mongo_insert_files import insert_files
conn = sqlite3.connect("FH.db")
crsr = conn.cursor()

OLD_HERO_PATH = r".\preComputedDatafiles\min_hero_stats.json"
OLD_MODE_PATH = r".\preComputedDatafiles\min_mode_stats.json"
NEW_HERO_PATH = r".\preComputedDatafiles\max_hero_stats.json"
NEW_MODE_PATH = r".\preComputedDatafiles\max_mode_stats.json"

def get_stats(join_table,MAX_or_MIN):
    sql = f"""
        SELECT UTCSeconds, username, platform, {join_table}.* FROM 
        (
        SELECT playerID,UTCSeconds,username,platform FROM
        (
        SELECT 
                playerID,
                username, 
                UTCSeconds,
                {MAX_or_MIN}(UTCSeconds) OVER (PARTITION BY username,platform) AS min_date,
                platform,
                wins,
                losses,
                timePlayed
                
                FROM (SELECT * FROM stat WHERE username IN (SELECT username FROM (SELECT username, count(username) AS cnt FROM stat GROUP BY username ) WHERE cnt > 2))
        )
        WHERE 
            UTCSeconds = min_date
        ) min_max
        INNER JOIN {join_table} ON {join_table}.playerID = min_max.playerID
    """
    crsr.execute(sql)
    return crsr.fetchall()

# get oldest mode data for each player
print("get oldest mode data for each player")
data = {}
data["data"] = get_stats("mode","MIN")
file = open(OLD_MODE_PATH,"w")
file.write(json.dumps(data) + "\n")
file.close()

# get newest mode data for each player
print("get newest mode data for each player")
file = open(NEW_MODE_PATH,"w")
data = {}
data["data"] = get_stats("mode","MAX")
file.write(json.dumps(data) + "\n")
file.close()

# get oldest hero data for each player
print("oldest hero data for each player")
file = open(OLD_HERO_PATH,"w")
data = {}
data["data"] = get_stats("hero","MIN")
file.write(json.dumps(data) + "\n")
file.close()

# get newest hero data for each player
print("get newest hero data for each player")
file = open(NEW_HERO_PATH,"w")
data = {}
data["data"] = get_stats("hero","MAX")
file.write(json.dumps(data) + "\n")
file.close()
data = {}

# convert the SQL dump into proper json
print("convert the SQL dump into proper json")
# get old data from files and combine it
print("get old data from files and combine it")
file = open(OLD_MODE_PATH,"r")
datafile = json.load(file)
file.close()
old_data = dd.sql_dump_to_json(datafile,"mode")

file = open(OLD_HERO_PATH,"r")
datafile = json.load(file)
file.close()

old_data = dd.sql_dump_to_json(datafile,"hero",users=old_data)


# get new data from files and combine it
print("get new data from files and combine it")
file = open(NEW_MODE_PATH,"r")
datafile = json.load(file)
file.close()
new_data = dd.sql_dump_to_json(datafile,"mode")

file = open(NEW_HERO_PATH,"r")
datafile = json.load(file)
file.close()

new_data = dd.sql_dump_to_json(datafile,"hero",users=new_data)

datafile = {}

# merge old and new data and write it into 1000 user files
print("segment data")
user_data = {}
count = 0
for player in new_data:
    player_data_o = old_data[player]
    player_data_n = new_data[player]
    user_data[player] = {
            "old" : player_data_o,
            "new" : player_data_n
        }
    
    if len(user_data) % 1000 == 0:
        file = open(rf"C:\Users\Jack Bowman\Documents\Programs\PytScripts\UserScraper\explorationScripts\WebsitePrep\segmented_user_data\user_data_{count}.json","w")
        file.write(json.dumps(user_data) + "\n")
        file.close()
        user_data = {}
        count += 1

user_data = {}
new_data = {}
old_data = {}

# go through each 1000 user file and insert it into the database
# insert_files()