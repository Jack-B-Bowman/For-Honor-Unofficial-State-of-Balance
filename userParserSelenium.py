import json
import time
import random
import sys
import threading
import sqlite3
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
mutex = threading.Lock()

arg = 0
if len(sys.argv) < 2:
    arg = 1
else: arg = int(sys.argv[1])

# read in the users csv
userFile = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\compiledUsers-06-27-1.csv","r")
usersFileLines = userFile.readlines()
userFile.close()
users = []

for line in usersFileLines:
    splitLine = line.split(",")
    platform = splitLine[0]
    username = splitLine[1][0:-1]
    splicedUsername = username.split("%20")
    splicedUsername = " ".join(splicedUsername)
    users.append((platform,username))


# shuffle the list for random selection from users
random.shuffle(users)


id = 0


nonExistantUsersFile = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\failedUsers.csv","r")
nonExistantUsersList = nonExistantUsersFile.readlines()
failedUsersDict = {}
for user in nonExistantUsersList:
    failedUsersDict[user] = True

def downloadThread(id):
    conn = sqlite3.connect("FH.db")
    crsr = conn.cursor()
    players = {}

    opts = uc.ChromeOptions()
    opts.headless = True
    opts.add_argument('--headless')
    opts.add_argument("--window-size=1020,900")  

    driver = uc.Chrome(options=opts, use_subprocess=True)
    num = 0
    while len(users) > 0:
        mutex.acquire()
        user = users.pop()
        mutex.release()

        skipUser = False
        timeForUpdate = False
        platform = user[0]
        username = user[1]

        splitUsername = username.split("%20")
        fortmattedUN = " ".join(splitUsername)
        

        sql = f"""SELECT username,platform,UTCSeconds from stat where username='{fortmattedUN}' and platform='{platform}'"""
        crsr.execute(sql)
        ans = crsr.fetchall()
        ans.sort(key=lambda y:y[2])
        # if the player exists
        timeForUpdate = False
        # does the player exist
        if len(ans) > 0: 
            # is the player inactive
            if len(ans) == 1:
                # if the player exists and is inactive update them once every 2 weeks
                if(time.time() - ans[-1][2] > (86400 * 14)):
                    timeForUpdate = True
            else:
                timeBetweenUpdates = ans[-1][2] - ans[-2][2]
                # if the player has not played in a month update them once a week
                if timeBetweenUpdates > 86400 * 30:
                    if(time.time() - ans[-1][2] > (86400 * 7)):
                        timeForUpdate = True
                # if the player has played in the last 30 days update them once a day
                else:
                    if(time.time() - ans[-1][2] > (86400 * 1)):
                        timeForUpdate = True
        if len(ans) == 0:
            timeForUpdate = True

        lineString = user[0] + "," + fortmattedUN + "\n"

        url = ""
        html_data = ""
        if lineString not in failedUsersDict and timeForUpdate:
            # catches any errors and skips the user if they gave an error. (this section would throw an error every thousand users or so)
            try:
                url = f'https://api.tracker.gg/api/v2/for-honor/standard/profile/{platform}/{username}?'
                driver.get(url)
                pre = driver.find_element(by=By.TAG_NAME, value="pre").text
                html_data = json.loads(pre)
                if 'errors' in html_data:
                    mutex.acquire()
                    failedUsersFile = open("failedUsers.csv","a")
                    failedUsersFile.write(platform + "," + username + "\n")
                    failedUsersFile.close()
                    mutex.release()
                else:
                    data = html_data['data']
            except Exception as e:
                print("GET error:\n", e)
                # failedUsersFile = open("failedUsers.csv","a")
                # failedUsersFile.write(platform + "," + username + "," + str(e))
                # failedUsersFile.close()
                skipUser = True
        else:
            skipUser = True
        


        # the stat tracker replaces spaces in the url with "%20" but the initial state json uses spaces when referencing the username
        # this simply reconstructs the actual username
        splitUsername = username.split("%20")
        username = " ".join(splitUsername)
        # mutex.acquire()
        if timeForUpdate and not skipUser:
            print(f"ThreadID : {id}\n  count : {str(num+1)} \n  user : {username}") # current user
        # mutex.release()
        if skipUser and lineString not in failedUsersDict and timeForUpdate:
                errorLog = open(f"errorLog-{id}.html","a")
                errorLog.write(driver.find_element_by_tag_name("body").text)
                errorLog.close()
        # provided all of the above went well
        if not skipUser:

            lowerCaseUN = username.lower()
            try:
                faction = data["metadata"]["factionKey"]
            except:
                skipUser = True 
            
            if skipUser and lineString not in failedUsersDict and timeForUpdate:
                    errorLog = open(f"errorLog-{id}.html","a")
                    errorLog.write(driver.find_element_by_tag_name("body").text)
                    errorLog.close()

            if not skipUser:
                # list of heros
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
                # player json format
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
                
                stats = { # each stats has the date (in seconds since epoch) along with the player's rep time played and PVP stats
                # these include total kills, deaths, assists, wins, and losses. As well as kills, deaths, assists, wins, and losses by mode
                # they also include kills, deaths, assists, wins, losses, and time played for each hero. I use time played as a substitute for rep.
                # these stats do not include K/D/A/W/L for each hero per mode. I cannot say for sure that player "A" has a 63% winrate in dominion as Berserker.
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
    
                # player["id"] = id
                # id += 1
                players[username] = {
                "psn" : [],
                "xbl" : [],
                "uplay" : []
                }
                stats["platform"] = platform
                stats["faction"] = faction

                # "segments" is about 1MB of json. it contains all the importand info that I want and a metric ton of data that i don't
                segments = data["segments"]
                for item in segments:
                    # if the current item in segments is a hero and that hero exists. OutlandersH030PirateQueen is the pirate and SamuraiH029Faceless is kyoshin
                    if item["type"] == "hero" and (item["metadata"]["name"] in heros or item["metadata"]["name"] == "OutlandersH030PirateQueen" or item["metadata"]["name"] == "SamuraiH029Faceless"):
                        name = item["metadata"]["name"]
                        if name == "OutlandersH030PirateQueen": name = "Pirate"
                        if name == "SamuraiH029Faceless": name = "Kyoshin"
                        heroStats = item["stats"]
                        stats["heros"][name]["wins"] = heroStats["wins"]["value"]
                        stats["heros"][name]["losses"] = heroStats["losses"]["value"]
                        stats["heros"][name]["kills"] = heroStats["killsP"]["value"]
                        stats["heros"][name]["deaths"] = heroStats["deathsP"]["value"]
                        stats["heros"][name]["assists"] = heroStats["assistsP"]["value"]
                        stats["heros"][name]["time"] = heroStats["timePlayed"]["value"]
                    
                    # this section contains the user's global stats
                    if item["type"] == "gameType":
                        if item["metadata"]["name"] == "Player vs. Player Overview":
                            globalStats = item["stats"]
                            stats["reputation"] = globalStats["reputation"]["value"]
                            stats["kills"] = globalStats["killsP"]["value"]
                            stats["deaths"] = globalStats["deathsP"]["value"]
                            stats["assists"] = globalStats["assistsP"]["value"]
                            stats["wins"] = globalStats["wins"]["value"]
                            stats["losses"] = globalStats["losses"]["value"]
                            stats["time"] = globalStats["timePlayed"]["value"]
                            stats["date"] = time.time()

                    # this section contains the gamemode stats
                    if item["metadata"]["name"] in modes:
                            mode = item["metadata"]["name"]
                            modeStats = item["stats"]
                            stats["modes"][mode]["wins"]   = modeStats["wins"]["value"]
                            stats["modes"][mode]["losses"] = modeStats["losses"]["value"]
                            stats["modes"][mode]["kills"]  = modeStats["killsP"]["value"]
                            stats["modes"][mode]["deaths"] = modeStats["deathsP"]["value"]
                            stats["modes"][mode]["assists"]= modeStats["assistsP"]["value"]
                            stats["modes"][mode]["time"]   = modeStats["timePlayed"]["value"]
                
                num += 1
                
                players[username][platform].append(stats)
                stats = {}
                # every 100 players write them to a file. this was to backup the data incase of a crash. I am not very good at this but it does save memory i think
                time.sleep(11)
                if(num % 100 == 0):
                    dataFile = open(f"C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\datafiles\\data{str(id)}-{str(num)}.json","a")
                    dataFile.write(json.dumps(players))
                    dataFile.close() 
                    players = {}

    dataFile = open(f"C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\datafiles\\dataFinal-{id}.json","a")
    dataFile.write(json.dumps(players))
    dataFile.close()
    players = {}

number = len(users)

threads = []
for n in range(arg):
    t = threading.Thread(target=downloadThread, args=[n])
    t.start()
    threads.append(t)

for item in threads:
    item.join()





