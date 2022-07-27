import sqlite3

# this is a script that takes player entries that are missing a hero due to that player having a "blank hero" on the hero page
# since the missing hero is always the player's least played it is acceptable to copy the data from the previous valid entry
# and use it for the missing hero

conn = sqlite3.connect("FH.db")
crsr = conn.cursor()

file = open("brokenUsers.csv","r")
players = file.readlines()
file.close()

for player in players:
    splitPlayer = player.split(",")
    username = splitPlayer[0]
    platform = splitPlayer[1]
    hero = splitPlayer[2][:-1]
    sql = f"""SELECT * from (SELECT stat.playerID,stat.username,stat.platform,stat.UTCSeconds,hero.* from stat join hero on stat.playerID=hero.playerID) 
where playerID in (SELECT playerID from stat WHERE username='{username}' and platform='{platform}')
order by playerID, name"""

    crsr.execute(sql)
    data = crsr.fetchall()
    entryData = {}
    lastID = -1
    playerData = []
    for line in data:
        playerID = line[0]
        entryHero = line[6]
        if lastID == -1:
            lastID = playerID
        elif lastID != playerID:
            playerData.append(entryData)
            entryData = {}
            lastID = playerID
        
        entryData[entryHero] = line
    

    for i in range(0,len(playerData)):
        line = playerData[i]
        heros = {}
        for hero in line:
            if hero in heros:
                heros[hero] += 1
            else:
                heros[hero] = 1
        
        
    print(entryData)
    