import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

from sqlalchemy import true


# file1 = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\newlyFormattedData.json","r")
# file2 = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\datafiles\\testing\\data8.json","r")
# data1 = json.load(file1)
# data2 = json.load(file2)
# dupes = {}
# activeDupes = {}
# numberOfDupes = 0
# numberOfActive = 0
# for user in data2:
#     if user in data1:
#         numberOfDupes += 1
#         dupes[user] = data1[user]
#         dupes[user + "New"] = data2[user]
#         for platform in data2[user]:
#             platformStatsList = data2[user][platform]
#             for stat in platformStatsList:
#                 isNew = True
#                 originalStats = data1[user][platform]
#                 for compareStat in originalStats:
#                     if compareStat["time"] == stat["time"]:
#                         isNew = False
#                 if isNew:
#                     numberOfActive += 1

# print(numberOfDupes)
# print(numberOfActive)

# file = open("tests.json","w")
# file.write(json.dumps(dupes,indent=4))
# file.close()

# theMap = {
# "Aramusha" : [],
# "Berserker" : [],
# "Black Prior" : [],
# "Centurion" : [],
# "Conqueror" : [],
# "Gladiator" : [],
# "Gryphon" : [],
# "Highlander" : [],
# "Hitokiri" : [],
# "Jiang Jun" : [],
# "Jormungandr" : [],
# "Kensei" : [],
# "Kyoshin" : [],
# "Lawbringer" : [],
# "Nobushi" : [],
# "Nuxia" : [],
# "Orochi" : [],
# "Peacekeeper" : [],
# "Pirate" : [],
# "Raider" : [],
# "Shaman" : [],
# "Shaolin" : [],
# "Shinobi" : [],
# "Shugoki" : [],
# "Tiandi" : [],
# "Valkyrie" : [],
# "Warden" : [],
# "Warlord" : [],
# "Warmonger" : [],
# "Zhanhu" : []
# }

theMap = {
"Aramusha" : {"wins": 0, "losses": 0},
"Berserker" : {"wins": 0, "losses": 0},
"Black Prior" : {"wins": 0, "losses": 0},
"Centurion" : {"wins": 0, "losses": 0},
"Conqueror" : {"wins": 0, "losses": 0},
"Gladiator" : {"wins": 0, "losses": 0},
"Gryphon" : {"wins": 0, "losses": 0},
"Highlander" : {"wins": 0, "losses": 0},
"Hitokiri" : {"wins": 0, "losses": 0},
"Jiang Jun" : {"wins": 0, "losses": 0},
"Jormungandr" : {"wins": 0, "losses": 0},
"Kensei" : {"wins": 0, "losses": 0},
"Kyoshin" : {"wins": 0, "losses": 0},
"Lawbringer" : {"wins": 0, "losses": 0},
"Nobushi" : {"wins": 0, "losses": 0},
"Nuxia" : {"wins": 0, "losses": 0},
"Orochi" : {"wins": 0, "losses": 0},
"Peacekeeper" : {"wins": 0, "losses": 0},
"Pirate" : {"wins": 0, "losses": 0},
"Raider" : {"wins": 0, "losses": 0},
"Shaman" : {"wins": 0, "losses": 0},
"Shaolin" : {"wins": 0, "losses": 0},
"Shinobi" : {"wins": 0, "losses": 0},
"Shugoki" : {"wins": 0, "losses": 0},
"Tiandi" : {"wins": 0, "losses": 0},
"Valkyrie" : {"wins": 0, "losses": 0},
"Warden" : {"wins": 0, "losses": 0},
"Warlord" : {"wins": 0, "losses": 0},
"Warmonger" : {"wins": 0, "losses": 0},
"Zhanhu" : {"wins": 0, "losses": 0}
}

# file = open("updatedUserStats04-28-2.json","r")
# data = json.load(file)
# file.close()

# user = "ohh phantoms"

# if user in data:
#     print("exists")

# file = open("mergedUserDataFile5.json","r")
# data = json.load(file)
# file.close()
# activeUsers = {}
# numPlayers = 0
# users = []
# for user in data:
#     numPlayers += 1
#     for platform in data[user]:
#         if len(data[user][platform]) > 0:
#                 username = user.split(" ")
#                 username = "%20".join(username)
#                 users.append((platform,username))



file = open("updatedUserStats04-28-5.json","r")
activeUsers = json.load(file)

totalMatches = 0
totalUsers = 0
for user in activeUsers:
    for platform in activeUsers[user]:
        if len(activeUsers[user][platform]) > 1:
            stats = activeUsers[user][platform]
            newlist = sorted(stats, key=lambda d: d['time'])
            first = newlist[0]
            last = newlist[-1]
            # print(json.dumps(first,indent=4))
            # print(json.dumps(last,indent=4))
            mode = "Elimination"
            modeDiff = (last["modes"][mode]["wins"] - first["modes"][mode]["wins"]) + (last["modes"][mode]["losses"] - first["modes"]["Dominion"]["losses"])
            totalDiff = (last["wins"] - first["wins"]) + (last["losses"] - first["losses"])
            # total = last["wins"] + last["losses"]
            if modeDiff > totalDiff * 0.5:
                totalUsers += 1
                for hero in first["heros"]:

                    winsDif   = last["heros"][hero]["wins"]   - first["heros"][hero]["wins"]
                    lossesDif = last["heros"][hero]["losses"] - first["heros"][hero]["losses"]

                    theMap[hero]["wins"] += winsDif
                    theMap[hero]["losses"] += lossesDif
                    # # winsDif   = last["heros"][hero]["wins"]  
                    # # lossesDif = last["heros"][hero]["losses"] 
                    
                    # if(winsDif != 0 and lossesDif != 0 and winsDif + lossesDif > 30 and last["heros"][hero]["time"] > 20000):  
                    #     totalMatches += winsDif + lossesDif                      
                    #     theMap[hero].append(winsDif/(winsDif + lossesDif))
print("n = " + str(totalMatches))
print("number of players = " + str(totalUsers))
print("winrate")
winrateList = []
for hero in theMap:
    # winRate = (np.median(theMap[hero])) * 100
    winRate = (theMap[hero]["wins"] / (theMap[hero]["wins"] + theMap[hero]["losses"])) * 100
    winrateList.append((hero,winRate, (theMap[hero]["wins"] + theMap[hero]["losses"])))
    # print(f"{hero} : {winRate:.2f}%")

winrateList.sort()
# winrateList.reverse()
for hero in winrateList:
    # print(f"{hero[1]}   :\t {hero[0]:.2f}% \t n = {hero[2]}" )
    print(f"{hero[0]}" )

for hero in winrateList:
    # print(f"{hero[1]}   :\t {hero[0]:.2f}% \t n = {hero[2]}" )
    print(f"{hero[1]}" )

for hero in winrateList:
    # print(f"{hero[1]}   :\t {hero[0]:.2f}% \t n = {hero[2]}" )
    print(f"{hero[2]}" )

# print("pickrate") 
# pickrateList = []
# for hero in theMap:
#     pickrate = ((theMap[hero]["wins"] + theMap[hero]["losses"]) / totalMatches) * 100
#     pickrateList.append((pickrate,hero))
    # print(f"{hero} : {pickrate:.2f}%")

# pickrateList.sort()
# pickrateList.reverse()
# print("n = " + str(totalMatches))
# print("number of players = " + str(totalUsers))
# for hero in pickrateList:
#     print(f"\t{hero[1]} : \t{hero[0]:.2f}%")


# file = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\datafiles\\mergedUserDataFile.json","r")
# data = json.load(file)
# missingDates = 0
# for user in data:
#     # theDate = time.time()
#     length = len(data[user])
#     i = 1
#     while i < length:
#         if data[user][0]["time"] == data[user][i]["time"]:
#             del data[user][i]
#             i -= 1
#             length -= 1
#         i += 1


        

# fixedFile = open("fixedFile2.json","w")
# fixedFile.write(json.dumps(data,indent=4))
# fixedFile.close()


# numberOfRepeats = 0
# numberOfActive = 0
# for user in data:
#     if len(data[user]) > 1:
#         if data[user][0]["kills"] < data[user][1]["kills"]:
#             numberOfActive +=1
#         numberOfRepeats += 1

# print(numberOfRepeats)
# print(numberOfActive)

# for player in data:
#     heros = player["heros"]
#     playerHeros = []
#     for key in heros:
#         playerHeros.append((key,heros[key]["time"]))
#     for hero in playerHeros:
#         theMap[hero[0]] += hero[1] / 31557600

# y = []
 
# # getting values against each value of y
# x = []
# for key in theMap:
#     x.append(theMap[key])
#     y.append(key)

# df = pd.DataFrame({
#     "time" : x,
#     "hero" : y,
# })

# df.sort_values("time")

# plt.barh(y, x)
 
# # setting label of y-axis
# plt.ylabel("Hero")
 
# # setting label of x-axis
# plt.xlabel("Time played (years)")
# plt.title("What Are The Most Popular Heros of All Time?")
# plt.show()

# savedNames = []
# for player in data:
#     savedNames.append(player["username"])

# savedNames = np.unique(savedNames)
# file = open("savedUsers04-22.txt","w")
# file.write(json.dumps(savedNames.tolist()))
# file.close()

# count = 0
# totalRep = 0
# for player in data:
#     totalRep += player["reputation"]
#     count += 1
# avgRep = totalRep/count
# print(f"avg rep = {avgRep}") 
# # 101

# file = open("updatedUserStats04-28-2.json","r")
# data = json.load(file)

# playerKDs = np.array([])
# playerReps = np.array([])

# playerPlatform = np.array([])
# numPSN = 0
# numXBL = 0
# numUPLAY = 0
# for player in data:
#     for platform in data[player]:
#         stats =  data[player][platform]
#         if len(stats) > 0:
#             kd =  stats[-1]["kills"] / stats[-1]["deaths"]
#             rep = stats[-1]["reputation"]

#         if rep < 500:
#             playerKDs = np.append(playerKDs,kd)
#             playerReps = np.append(playerReps,rep)

# playerKDs = np.append(playerKDs,12)
# playerReps = np.append(playerReps,9)
# playerKDs = np.append(playerKDs,10.23)
# playerReps = np.append(playerReps,99)


# plt.rcdefaults()
# fig, ax = plt.subplots()

# # Example data
# platforms = ['PSN', 'XBOX', 'PC']
# values = [(numPSN/(numPSN+numUPLAY+numXBL)) * 100,(numXBL/(numPSN+numUPLAY+numXBL)) * 100 ,(numUPLAY/(numPSN+numUPLAY+numXBL)) * 100]
# plt.bar(platforms, values)
# ax.set_xlabel('Platform')
# ax.set_ylabel("Percent of users (%)")
# ax.set_title('How are players distributed?')
# plt.show()

# print(len(playerKDs))

# z = np.polyfit(playerReps, playerKDs, 1)
# p = np.poly1d(z)
# plt.xlabel('player rep', fontsize=20)
# plt.ylabel('player KD', fontsize=20)
# plt.scatter(playerReps, playerKDs, s=1)
# plt.plot(playerReps, p(playerReps))
# plt.show()

# reps = np.array([])
# for player in data:
#     reps = np.append(reps,player["reputation"])

# print(np.median(reps))
# print(min(reps))