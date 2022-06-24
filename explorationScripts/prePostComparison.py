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
preSeasonList.sort(key=lambda y:y[2])
postSeasonList = heroStatsJsonToList(postSeasonData)
postSeasonList.sort(key=lambda y:y[2])
preSeasonList = [tuple for x in postSeasonList for tuple in preSeasonList if tuple[0] == x[0]]

preSeasonList.reverse()
postSeasonList.reverse()

# preSeasonList = list(filter(lambda x: True if x[0] in ["Conqueror","Pirate","Shaolin"] else False, preSeasonList))
# postSeasonList = list(filter(lambda x: True if x[0] in ["Conqueror","Pirate","Shaolin"] else False, postSeasonList))

plt.rcdefaults()
fig, ax = plt.subplots()

# graph postSeason
names = [i[0] for i in postSeasonList]
winrates = [i[1] for i in postSeasonList]
pickrates = [i[2] for i in postSeasonList]


y_pos = np.arange(len(names))

ax.barh(y_pos, pickrates, align='center', label="Current Season",color='#dd5223')

for i, v in enumerate(pickrates):
    b = float(v)
    ax.text(v + 0.15, i + 0.14, f"{b:.2f}%",
            color = 'black', fontweight = 'bold')

# ax.barh(y_pos, pickrates, align='center',height=0.3)

# for i, v in enumerate(pickrates):
#     b = float(v)
#     ax.text(v + 0.1, i + 0.25, f"{b:.2f}%",
#             color = 'white', fontweight = 'bold')

# graph preSeason

names = [i[0] for i in preSeasonList]
winrates = [i[1] for i in preSeasonList]
pickrates = [i[2] for i in preSeasonList]


y_pos = np.arange(len(names))

ax.barh(y_pos, pickrates, align='center',height=0.5, label="Last Season",color="#ddaf23")

for i, v in enumerate(pickrates):
    b = float(v)
    if abs(b - postSeasonList[i][2]) > 1.0:
        ax.text(v + 0.15, i + 0.14, f"{b:.2f}%",
                color = 'black', fontweight = 'bold')

# ax.barh(y_pos, pickrates, align='center',height=0.15)

# for i, v in enumerate(pickrates):
#     b = float(v)
#     ax.text(v + 0.1, i + 0.25, f"{b:.2f}%",
#             color = 'white', fontweight = 'bold')

ax.set_yticks(y_pos)
ax.set_yticklabels(names)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Pickrate (%)')
ax.set_xlim(xmin=0)
ax.set_xlim(xmax=20)
ax.set_title('What is The Pickrate by Hero')
ax.legend()

# ticks = list(range(0,10)) + list(range(30,70))

# plt.xticks(ticks,[str(i) for i in ticks])
plt.show()

