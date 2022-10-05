from select import select
import numpy as np
import json
import sqlite3
conn = sqlite3.connect("FH.db")
crsr = conn.cursor()

getNamesSQL = """SELECT username,platform from stat group by username,platform"""
crsr.execute(getNamesSQL)
names = np.array(crsr.fetchall())

sussed = {}
num = 0
print("processing...")
for player in names:

    # if player[0] == 'Lucky_Arian' and player[1] == 'uplay':
    #     print("stop")

    num += 1
    if num % 1000 == 0:
        print(f"\r {(num/len(names))*100:.0f}",end="")
    getPlayer = f"""select username, platform, UTCSeconds, CAST(wins AS INT) AS wins, CAST(losses AS INT) AS losses from stat where username = '{player[0]}' and platform = '{player[1]}' order by UTCSeconds"""
    crsr.execute(getPlayer)
    ans = crsr.fetchall()
    firstStats = ans[0][3:5]
    lastStats = ans[-1][3:5]

    historicMatches = firstStats[1] + firstStats[0]
    recentWins = lastStats[0] - firstStats[0]
    recentLosses = lastStats[1] - firstStats[1]
    recentMatches = recentWins + recentLosses

    if recentMatches > 0 and firstStats[1] + firstStats[0] > 0:
        historicWinrate = (firstStats[0] / (firstStats[1] + firstStats[0])) * 100

        recentWinrate = (recentWins / recentMatches) * 100

        if recentMatches > 100 and historicMatches > 100 and recentWinrate - historicWinrate > 15:
            sussed[player[0] + "," + player[1]] = {
                "historic matches"  : historicMatches,
                "recent matches"    : recentMatches,
                "historic winrate"  : historicWinrate,
                "recent winrate"    : recentWinrate,
                "winrate diff"      : recentWinrate - historicWinrate 
            }
print()
file = open('C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\preComputedDatafiles\\susPlayers.json','w')
file.write(json.dumps(sussed, indent=4))
file.close()
print("Done")