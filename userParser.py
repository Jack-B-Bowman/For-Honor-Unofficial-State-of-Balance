import re
import json
import time
import requests
import random

# read in the users csv
userFile = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\users.csv","r")
usersFileLines = userFile.readlines()
userFile.close()
users = []
#split the csv into the platform and username of each user

userToResumeAt = "ekel_hd"
for line in usersFileLines:
    resumePointReached = False
    splitLine = line.split(",")
    platform = splitLine[0]
    username = splitLine[1]

    if username == userToResumeAt or resumePointReached:
        print("resuming at user: " )
        users.append((platform,username))
# shuffle the list for random selection from 250 000 users
random.shuffle(users)

players = []
successfulUsernames = []
num = 0
id = 0
# for each user
for user in users:
    skipUser = False

    platform = user[0]
    username = user[1][0:-1].lower()

    try:

        url = f'https://tracker.gg/for-honor/profile/{platform}/{username}/pvp'
        html_data = requests.get(url).text
    except:
        print("GET error")
        skipUser = True

    
    # error handling for going over access limit. will retry every ten seconds
    attempts = 0
    while len(html_data) < 1000 and not skipUser:
        time.sleep(5)
        print("error on " + username)
        url = f'https://tracker.gg/for-honor/profile/{platform}/{username}/pvp'
        html_data = requests.get(url).text
        attempts += 1
        time.sleep(5)
        if attempts >= 5:
            skipUser = True
    
    if not skipUser: 
        successfulUsernames.append(username)

    splitUsername = username.split("%20")
    username = " ".join(splitUsername)
    print(str(num + 1) + " : " + username)

    # strip the initial state JSON from the HTML page
    try:

        data = re.search(r"window\.__INITIAL_STATE__=({.*});", html_data).group(1)
        data = json.loads(data)
        # strip the useless stuff from the state
        data = data["stats"]["standardProfiles"]
    except:
        print("group error")
        skipUser = True

    try:
        if data[f"for-honor|{platform}|{username}"]["status"] != 0: 
            skipUser = True
            print(username + " : status error")
    except:
        ...

    if not skipUser:



        file = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\pvp2.json","w")
        file.write(json.dumps(data, indent=4))
        file.close()



        data = data[f"for-honor|{platform}|{username}"]


        faction = data["metadata"]["factionKey"]

        heros = [
        "Aramusha",
        "Berserker",
        "Black Prior",
        "Centurion",
        "Conqueror",
        "Gladiator",
        "Gryphon",
        "Highlander",
        "Hitokiri",
        "Jiang Jun",
        "Jormungandr",
        "Kensei",
        "Kyoshin",
        "Lawbringer",
        "Nobushi",
        "Nuxia",
        "Orochi",
        "Peacekeeper",
        "Pirate",
        "Raider",
        "Shaman",
        "Shaolin",
        "Shinobi",
        "Shugoki",
        "Tiandi",
        "Valkyrie",
        "Warden",
        "Warlord",
        "Warmonger",
        "Zhanhu"
        ]

        modes = ["Dominion","Duel","Breach","Elimination","Skirmish"]

        player = {
            "id" : 0,
            "platform" : "",
            "username" : "",
            "faction" : "",
            "reputation" : 0,
            "kills" : 0,
            "deaths": 0,
            "assists" : 0,
            "wins" : 0,
            "losses": 0,
            "time" : 0,
            "date" : time.time(),

            "modes" : {
                "Dominion" : {
                    "wins" : 0,
                    "losses" : 0,
                    "kills" : 0,
                    "deaths": 0,
                    "assists": 0,
                    "time" : 0
                },
                "Duel" : {
                    "wins" : 0,
                    "losses" : 0,
                    "kills" : 0,
                    "deaths": 0,
                    "assists": 0,
                    "time" : 0
                },
                "Breach" : {
                    "wins" : 0,
                    "losses" : 0,
                    "kills" : 0,
                    "deaths": 0,
                    "assists": 0,
                    "time" : 0
                },
                "Elimination" : {
                    "wins" : 0,
                    "losses" : 0,
                    "kills" : 0,
                    "deaths": 0,
                    "assists": 0,
                    "time" : 0
                },
                "Skirmish" : {
                    "wins" : 0,
                    "losses" : 0,
                    "kills" : 0,
                    "deaths": 0,
                    "assists": 0,
                    "time" : 0
                }
            },
            "heros" : {
                "Aramusha" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Berserker" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Black Prior" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Centurion" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Conqueror" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Gladiator" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Gryphon" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Highlander" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Hitokiri" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Jiang Jun" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Jormungandr" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Kensei" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Kyoshin" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Lawbringer" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Nobushi" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Nuxia" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Orochi" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Peacekeeper" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Pirate" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Raider" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Shaman" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Shaolin" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Shinobi" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Shugoki" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Tiandi" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Valkyrie" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Warden" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Warlord" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Warmonger" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
                "Zhanhu" : {
                    "time" : 0,
                    "wins" : 0,
                    "losses":0,
                    
                    "kills": 0,
                    "deaths":0,
                    "assists":0
                },
            }

        }
        
        
        player["id"] = id
        id += 1
        player["platform"] = platform
        player["username"] = username
        player["faction"] = faction

        segments = data["segments"]
        for item in segments:
            if item["type"] == "hero" and (item["metadata"]["name"] in heros or item["metadata"]["name"] == "OutlandersH030PirateQueen" or item["metadata"]["name"] == "SamuraiH029Faceless"):
                name = item["metadata"]["name"]
                if name == "OutlandersH030PirateQueen": name = "Pirate"
                if name == "SamuraiH029Faceless": name = "Kyoshin"
                heroStats = item["stats"]
                player["heros"][name]["wins"] = heroStats["wins"]["value"]
                player["heros"][name]["losses"] = heroStats["losses"]["value"]
                player["heros"][name]["kills"] = heroStats["killsP"]["value"]
                player["heros"][name]["deaths"] = heroStats["deathsP"]["value"]
                player["heros"][name]["assists"] = heroStats["assistsP"]["value"]
                player["heros"][name]["time"] = heroStats["timePlayed"]["value"]
            
            if item["type"] == "gameType":
                if item["metadata"]["name"] == "Player vs. Player Overview":
                    stats = item["stats"]
                    player["reputation"] = stats["reputation"]["value"]
                    player["kills"] = stats["killsP"]["value"]
                    player["deaths"] = stats["deathsP"]["value"]
                    player["assists"] = stats["assistsP"]["value"]
                    player["wins"] = stats["wins"]["value"]
                    player["losses"] = stats["losses"]["value"]
                    player["time"] = stats["timePlayed"]["value"]

            if item["metadata"]["name"] in modes:
                    mode = item["metadata"]["name"]
                    modeStats = item["stats"]
                    player["modes"][mode]["wins"]   = modeStats["wins"]["value"]
                    player["modes"][mode]["losses"] = modeStats["losses"]["value"]
                    player["modes"][mode]["kills"]  = modeStats["killsP"]["value"]
                    player["modes"][mode]["deaths"] = modeStats["deathsP"]["value"]
                    player["modes"][mode]["assists"]= modeStats["assistsP"]["value"]
                    player["modes"][mode]["time"]   = modeStats["timePlayed"]["value"]
        
        num += 1
        
        players.append(player)
        if(num % 100 == 0):
            dataFile = open(f"C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\datafiles\\data{str(num)}.json","a")
            dataFile.write(json.dumps(players, indent=4))
            dataFile.close()
            successfulUsernames = []
            players = []
        






