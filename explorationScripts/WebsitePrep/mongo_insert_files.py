import json
import pymongo
import os
def insert_files():
    pass_file = open(r"C:\Users\Jack Bowman\Documents\Programs\PytScripts\UserScraper\explorationScripts\WebsitePrep\passwords.json","r")
    conn_string = json.load(pass_file)["connstring"]

    myclient = pymongo.MongoClient(conn_string)
    mydb = myclient["user_data_db"]
    mycol = mydb["user_data_col"]

    dir = r"C:\Users\Jack Bowman\Documents\Programs\PytScripts\UserScraper\explorationScripts\WebsitePrep\segmented_user_data"
    count = 0
    for filename in os.listdir(dir):
        file = open(dir + "\\" + filename,"r")
        data = json.load(file)
        file.close()
        list_of_entries = []
        for player in data:
            player_data = data[player]
            entry = {"_id" : player, "old" : player_data["old"], "new" : player_data["new"]}
            list_of_entries.append(entry)
        try:
            x = mycol.insert_many(list_of_entries)
            print(x.inserted_ids)
        except:
            ...
        count += 1

    