import json


file = open(r"C:\Users\Jack Bowman\Documents\Programs\PytScripts\UserScraper\explorationScripts\WebsitePrep\new_data.json","r")
new_data = json.load(file)
file.close()

file = open(r"C:\Users\Jack Bowman\Documents\Programs\PytScripts\UserScraper\explorationScripts\WebsitePrep\old_data.json","r")
old_data = json.load(file)
file.close()

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