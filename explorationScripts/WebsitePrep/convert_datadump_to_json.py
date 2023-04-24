import json

user_files = [
    r"C:\Users\Jack Bowman\Documents\Programs\PytScripts\UserScraper\preComputedDatafiles\max_hero_stats.json",
    r"C:\Users\Jack Bowman\Documents\Programs\PytScripts\UserScraper\preComputedDatafiles\min_hero_stats.json",
    r"C:\Users\Jack Bowman\Documents\Programs\PytScripts\UserScraper\preComputedDatafiles\min_mode_stats.json",
    r"C:\Users\Jack Bowman\Documents\Programs\PytScripts\UserScraper\preComputedDatafiles\max_mode_stats.json",

]



# data_type is "mode" or "hero"
# users is an empty dict or the dict of other users
def sql_dump_to_json(json_dump,data_type,users={}): 


    sub_selector_string = data_type
    for player in json_dump["data"]:

        stats = {
        "wins" : 0,
        "losses": 0,
        "kills" : 0,
        "deaths" : 0,
        "assists" : 0,
        "time_played" : 0
        } 

        username = player[1]
        platform = player[2]
        name = player[5]
        stats["kills"] = player[6]
        stats["deaths"] = player[7]
        stats["assists"] = player[8]
        stats["wins"] = player[9]
        stats["losses"] = player[10]
        stats["time_played"] = player[11]

        player_key = username + ":" + platform

        if player_key not in users:
            users[player_key] = {
                "hero" : {},
                "mode" : {}
            }
        
        users[player_key][sub_selector_string][name] = stats
        # print(json.dumps(users,indent=4))
    
    return users


file = open(user_files[2],"r")
datafile = json.load(file)
file.close()
users = sql_dump_to_json(datafile,"mode")

file = open(user_files[1],"r")
datafile = json.load(file)
file.close()

users = sql_dump_to_json(datafile,"hero",users=users)
file_path = r"C:\Users\Jack Bowman\Documents\Programs\PytScripts\UserScraper\explorationScripts\WebsitePrep\old_data.json"
file = open(file_path,"w")
file.write(json.dumps(users) + "\n")
file.close()