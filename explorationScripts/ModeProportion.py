# finds the recent proportion of matches played in each mode in dataset
# e.g. 70% Dominion 20% Duel 10% Brawl
import time
import json
import sqlite3
conn = sqlite3.connect("FH.db")
crsr = conn.cursor()

# seasonStartDate = 1655395200 # true season start
seasonStartDate = 1656547619 # post conq nerf 
# seasonStartDate = 1658970014
seasonStartDate = 1659742490

# gets number of matches in each mode for each player
SQLString = f"""

SELECT 	stat.username,
		stat.platform,
		stat.UTCSeconds,
        stat.wins + stat.losses as totalMatches,
		mode.name,mode.wins + mode.losses as matches  
		
	from mode inner join stat on mode.playerID = stat.playerID 
	where stat.UTCSeconds > {seasonStartDate}
	order by username,platform,name,UTCSeconds
    --limit 1000
"""
preTime = time.time()
crsr.execute(SQLString)
ans = crsr.fetchall()
print(f"Query Execution time = {(time.time() - preTime):.2f} seconds")

statsByPlayer = {}

lastNamePlatform = ""
print("Separating users...")
n = 0
for stat in ans:
    n += 1
    if n % 1000 == 0:
        print(f"\r{(n / len(ans)) * 100:.0f}% complete",end="")
    username = stat[0]
    platform = stat[1]
    UTCSeconds = stat[2]
    totalMatches = stat[3]
    modeName = stat[4]
    modeMatches = stat[5]

    namePlatform = username + platform
    if namePlatform in statsByPlayer:
        statsByPlayer[namePlatform].append((UTCSeconds,totalMatches,modeName,modeMatches))
    else:
        statsByPlayer[namePlatform] = []
        statsByPlayer[namePlatform].append((UTCSeconds,totalMatches,modeName,modeMatches))

print("getting totals")
totals = {
    "Breach" : 0,
    "Dominion" : 0,
    "Duel" : 0,
    "Elimination" : 0,
    "Skirmish" : 0,
    "Brawl+Ranked" : 0,
    "Total" : 0,
}
for player in statsByPlayer:
    results = statsByPlayer[player]
    modes = {}
    for item in results:
        mode = item[2]
        modeMatches = item[3]
        totalMatches = item[1]
        if mode not in modes:
            modes[mode] = [modeMatches]
        else:
            modes[mode].append(modeMatches)
        if "Total" not in modes:
            modes["Total"] = [totalMatches]
        else:
            if totalMatches > modes["Total"][-1]:
                modes["Total"].append(totalMatches)
    
    calculatedTotal = 0
    try:
        localTotal = modes["Total"][-1] - modes["Total"][0]
    except:
        localTotal = 0
    if localTotal < 0:
        print("wat")
    totals["Total"] += localTotal
    for mode in modes:
        matchList = sorted(modes[mode])
        matchesPlayed = matchList[-1] - matchList[0]
        if matchesPlayed > 0:
            calculatedTotal += matchesPlayed
            totals[mode] += matchesPlayed
    if calculatedTotal < localTotal:
        totals["Brawl+Ranked"] += localTotal - calculatedTotal


print(json.dumps(totals,indent=4))

        


