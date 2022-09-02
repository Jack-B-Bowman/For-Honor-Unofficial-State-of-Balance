from locale import currency
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import json
from datetime import datetime
conn = sqlite3.connect("FH.db")
crsr = conn.cursor()

theMap = {
"Aramusha" : [0,0],
"Berserker" : [0,0],
"Black Prior" : [0,0],
"Centurion" : [0,0],
"Conqueror" : [0,0],
"Gladiator" : [0,0],
"Gryphon" : [0,0],
"Highlander" : [0,0],
"Hitokiri" : [0,0],
"Jiang Jun" : [0,0],
"Jormungandr" : [0,0],
"Kensei" : [0,0],
"Kyoshin" : [0,0],
"Lawbringer" : [0,0],
"Nobushi" : [0,0],
"Nuxia" : [0,0],
"Orochi" : [0,0],
"Peacekeeper" : [0,0],
"Pirate" : [0,0],
"Raider" : [0,0],
"Shaman" : [0,0],
"Shaolin" : [0,0],
"Shinobi" : [0,0],
"Shugoki" : [0,0],
"Tiandi" : [0,0],
"Valkyrie" : [0,0],
"Warden" : [0,0],
"Warlord" : [0,0],
"Warmonger" : [0,0],
"Zhanhu" : [0,0],
"Medjay" : [0,0]
}

totalMatches = 0
theMap2 = {
"Aramusha" : 0,
"Berserker" : 0,
"Black Prior" : 0,
"Centurion" : 0,
"Conqueror" : 0,
"Gladiator" : 0,
"Gryphon" : 0,
"Highlander" : 0,
"Hitokiri" : 0,
"Jiang Jun" : 0,
"Jormungandr" : 0,
"Kensei" : 0,
"Kyoshin" : 0,
"Lawbringer" : 0,
"Nobushi" : 0,
"Nuxia" : 0,
"Orochi" : 0,
"Peacekeeper" : 0,
"Pirate" : 0,
"Raider" : 0,
"Shaman" : 0,
"Shaolin" : 0,
"Shinobi" : 0,
"Shugoki" : 0,
"Tiandi" : 0,
"Valkyrie" : 0,
"Warden" : 0,
"Warlord" : 0,
"Warmonger" : 0,
"Zhanhu" : 0,
"Medjay" : 0
}

playerIDs = []
# 1656547619
sql = """

SELECT stat.playerID, stat.username, stat.platform, stat.wins as totalWins, stat.losses as totalLosses, mode.wins as domWins, mode.losses as domLosses
 from stat INNER join mode WHERE mode.playerID = stat.playerID and mode.name='Dominion' and stat.UTCSeconds > 0 and username in (
 
SELECT username from 
(SELECT username, count(username) as num from stat 
GROUP by username)
where num > 1

 )
ORDER by username

"""
print("Selecting dominion stats of active users")
crsr.execute(sql)
ans = crsr.fetchall()

print("Checking results for pairs with 100% dominion matches")
for entry in range(1,len(ans)):

    if entry % 100000 == 0:
        print(f"{(entry/len(ans)) * 100:.2f}% Complete")

    playerStat = ans[entry]
    lastPlayerStat = ans[entry - 1]
    currentUN = playerStat[1]
    lastUN = lastPlayerStat[1]

    if currentUN == lastUN:
        totalMatchDif = (playerStat[3] + playerStat[4]) - (lastPlayerStat[3] + lastPlayerStat[4])
        domMatchDif = (playerStat[5] + playerStat[6]) - (lastPlayerStat[5] + lastPlayerStat[6])
        if totalMatchDif == domMatchDif:
            playerIDs.append((lastPlayerStat[0],playerStat[0]))
    else:
        ...



print("Getting wins and losses for each hero")
i = 0
for pair in playerIDs:
    i += 1
    if i % 10000 == 0:
        print(f"{(i/len(playerIDs)) * 100:.2f}%")
    earlyID = pair[0]
    lateID = pair[1]
    selectSQL = f"""SELECT * from hero where playerID = {earlyID} or playerID = {lateID}"""
    crsr.execute(selectSQL)
    ans = crsr.fetchall()
    earlyStats = {}
    lateStats = {}

    for item in ans:

        
        if item[1] == earlyID:
            earlyStats[item[2]] = item[3:]
        else:
            lateStats[item[2]] = item[3:]

    for hero in earlyStats:
        try:
            res = tuple(map(lambda i, j: i - j, lateStats[hero], earlyStats[hero]))
            theMap[hero][0] += res[3]
            theMap[hero][1] += res[4]
            theMap2[hero] += res[3] + res[4]
        except Exception as e:
            # print(e)
            ...

winrateList = []
for hero in theMap:
    winrate = (theMap[hero][0] / (theMap[hero][1] + theMap[hero][0])) * 100
    winrateList.append((hero,winrate))


winrateList.sort(key=lambda y:y[1])
winrateList.reverse()
for hero in winrateList:
    print(f"{hero[0]}   :\t {hero[1]:.2f}%, n={theMap2[hero[0]]}" )
    # print(f"{hero[0]}" )

# for hero in winrateList:
#     # print(f"{hero[1]}   :\t {hero[0]:.2f}% \t n = {hero[2]}" )
#     print(f"{hero[1]}" )

# for hero in winrateList:
#     # print(f"{hero[1]}   :\t {hero[0]:.2f}% \t n = {hero[2]}" )
#     print(f"{hero[2]}" )

plt.rcdefaults()
fig, ax = plt.subplots()


names = [i[0] for i in winrateList]
winrates = [i[1] for i in winrateList]

y_pos = np.arange(len(names))


ax.barh(y_pos, winrates, align='center')

for i, v in enumerate(winrates):
    b = float(v)
    ax.text(v + 0.1, i + 0.25, f"{b:.2f}%",
            color = 'black', fontweight = 'bold')


ax.set_yticks(y_pos)
ax.set_yticklabels(names)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Winrate (%)')
ax.set_xlim(xmin=0)
ax.set_xlim(xmax=65)
ax.set_title('What is The Winrate By Hero 100% Dominion')

ticks = list(range(0,10)) + list(range(50,70))

plt.xticks(ticks,[str(i) for i in ticks])
plt.show()