import json
import matplotlib.pyplot as plt
import numpy as np

preSeasonFile  = open("preComputedDatafiles\\preSeasonData.json","r")
postSeasonFile = open("preComputedDatafiles\\postSeasonData.json","r")

def heroStatsJsonToList(data):
    dataList = []
    for hero in data:
        winrate = data[hero][0]
        pickrate = data[hero][1]
        dataList.append((hero,winrate,pickrate))
    return dataList

preSeasonData = json.load(preSeasonFile)
postSeasonData = json.load(postSeasonFile)

preSeasonList = heroStatsJsonToList(preSeasonData)
preSeasonList.sort(key=lambda y:y[1])
postSeasonList = heroStatsJsonToList(postSeasonData)
postSeasonList.sort(key=lambda y:y[1])
preSeasonList = [tuple for x in postSeasonList for tuple in preSeasonList if tuple[0] == x[0]]

preSeasonList.reverse()
postSeasonList.reverse()

# preSeasonList = list(filter(lambda x: True if x[0] in ["Conqueror","Pirate","Shaolin"] else False, preSeasonList))
# postSeasonList = list(filter(lambda x: True if x[0] in ["Conqueror","Pirate","Shaolin"] else False, postSeasonList))

plt.rcdefaults()
fig, ax = plt.subplots()

# graph postSeason
names = [i[0] for i in preSeasonList]
winrates = np.array([i[1] for i in preSeasonList])
winrateMean = np.mean(winrates)
pickrates = [i[2] for i in preSeasonList]


y_pos = np.arange(len(names))

ax.barh(y_pos, winrates, align='center', label="Afeera Release")

for i, v in enumerate(winrates):
    b = float(v)
    if abs(b - postSeasonList[i][1]) > 1.0:
        ax.text(v + 0.15, i + 0.14, f"{b:.2f}%",
                color = 'black', fontweight = 'bold')

# ax.barh(y_pos, pickrates, align='center',height=0.3)

# for i, v in enumerate(pickrates):
#     b = float(v)
#     ax.text(v + 0.1, i + 0.25, f"{b:.2f}%",
#             color = 'white', fontweight = 'bold')

# graph preSeason

names = [i[0] for i in postSeasonList]
winrates = [i[1] for i in postSeasonList]
pickrates = [i[2] for i in postSeasonList]


y_pos = np.arange(len(names))

ax.barh(y_pos, winrates, align='center',height=0.5, label="Dodge Attacks and Jorm Rework")

for i, v in enumerate(winrates):
    b = float(v)
    # if abs(b - preSeasonList[i][1]) > 1.0:
    ax.text(v + 0.15, i + 0.14, f"{b:.1f}%",
                color = 'black', fontweight = 'bold')

# ax.barh(y_pos, pickrates, align='center',height=0.15)

# for i, v in enumerate(pickrates):
#     b = float(v)
#     ax.text(v + 0.1, i + 0.25, f"{b:.2f}%",
#             color = 'white', fontweight = 'bold')

ax.set_yticks(y_pos)
ax.set_yticklabels(names)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Winrate (%)')
ax.set_xlim(xmin=40)
ax.set_xlim(xmax=65)
ax.set_title('Afeera release Vs Jorm rework / light parry')
ax.legend(loc='lower right')

# ticks = list(range(0,10)) + list(range(30,70))

# plt.xticks(ticks,[str(i) for i in ticks])
plt.show()

