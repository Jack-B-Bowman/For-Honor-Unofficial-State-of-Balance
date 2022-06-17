import json



stats = { # each stats has the date (in seconds since epoch) along with the player's rep time played and PVP stats
         # these include total kills, deaths, assists, wins, and losses. As well as kills, deaths, assists, wins, and losses by mode
         # they also include kills, deaths, assists, wins, losses, and time played for each hero. I use time played as a substitute for rep.
         # these stats do not include K/D/A/W/L for each hero per mode. I cannot say for sure that player "A" has a 63% winrate in dominion as Berzerker.
         # this kind of stat could be approximated by using players that play almost exclusivly that mode though
            "date" : 0,
            "platform" : "",
            "faction" : "",
            "reputation" : 0,
            "kills" : 0,
            "deaths": 0,
            "assists" : 0,
            "wins" : 0,
            "losses": 0,
            "time" : 0,
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

# singlePlayer = [stats,stats,stats] #this list holds all the stats for the player
singlePlayer = [] #this list holds all the stats for the player

# allPlayers = {
#     "username" : singlePlayer
# }
allPlayers = {}

fileToFormat = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\mergedFile04-23-1.json")
allTheStuff = json.load(fileToFormat)
fileToFormat.close()

currentID = 0
for player in allTheStuff:
    username = player["username"]
    platform = player["platform"]
    faction  = player["faction"]
    reputation = player["reputation"]
    kills = player["kills"]
    deaths = player["deaths"]
    assists = player["assists"]
    wins = player["wins"]
    losses = player["losses"]
    time = player["time"]
    date = player["date"]
    modes = player["modes"]
    heros = player["heros"]

    stats["date"] = date
    stats["platform"] = platform
    stats["faction"] = faction
    stats["reputation"] = reputation
    stats["kills"] = kills
    stats["deaths"] = deaths
    stats["assists"] = assists
    stats["wins"] = wins
    stats["losses"] = losses
    stats["time"] = time
    stats["modes"] = modes
    stats["heros"] = heros

    allPlayers[username] = []
    allPlayers[username].append(stats)
    stats = {}

file = open("userDataFile1.json","w")
file.write(json.dumps(allPlayers, indent=4))
file.close()