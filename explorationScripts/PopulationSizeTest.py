import sqlite3
import random
conn = sqlite3.connect("FH.db")
crsr = conn.cursor()

sql = """select username,platform from (select username,platform, count(username) as userCount from stat group by username) where userCount > 1"""

crsr.execute(sql)
ans = crsr.fetchall()
winsLosses = {
    "xbl" : {
        "wins" : 0,
        "losses" : 0,
        "players": 0
    },
        "psn" : {
        "wins" : 0,
        "losses" : 0,
        "players": 0
    },
    "uplay" : {
        "wins" : 0,
        "losses" : 0,
        "players": 0
    },

}


numberOfTests = 1000000

for i in range(numberOfTests):
    if i % 100000 == 0:
        print(f"{((i/numberOfTests) * 100):.2f}% complete")
    playersW = ["","","",""]
    playersL = ["","","",""]
    fourStack = False
    randomNum = random.random()
    plat = random.choice(ans)[1]
    if plat == "xbl" and randomNum > 0.80: 
        fourStack = True
    if plat == "psn" and randomNum > 0.95: 
        fourStack = True
    if plat == "uplay" and randomNum > 0.95: 
        fourStack = True
    if fourStack:
        playersW[0] = plat
        playersW[1] = plat
        playersW[2] = plat
        playersW[3] = plat
    else:
        playersW[0] = plat
        for j in range(1,4):
            plat = random.choice(ans)[1]
            playersW[j] = plat
    for k in range(4):
        playersL[k] = random.choice(ans)[1]
    
    for player in playersW:
        winsLosses[player]["wins"] += 1
        winsLosses[player]["players"] += 1

    for player in playersL:
        winsLosses[player]["losses"] += 1
        winsLosses[player]["players"] += 1
    

    

xblWinrate = winsLosses['xbl']["wins"] / (winsLosses['xbl']["wins"] + winsLosses['xbl']["losses"]) * 100
psnWinrate = winsLosses['psn']["wins"] / (winsLosses['psn']["wins"] + winsLosses['psn']["losses"]) * 100
uplayWinrate = winsLosses['uplay']["wins"] / (winsLosses['uplay']["wins"] + winsLosses['uplay']["losses"]) * 100
print(f"xbl winrate = {xblWinrate:.2f}")
print(f"psn winrate = {psnWinrate:.2f}")
print(f"uplay winrate = {uplayWinrate:.2f}")