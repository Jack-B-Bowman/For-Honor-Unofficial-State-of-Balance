import re
import time

heroNames = {
                "Aramusha" : "Aramusha" ,
                "Berserker" : "Berserker" ,
                "Black Prior" : "Black Prior" ,
                "Centurion" : "Centurion"  ,
                "Conqueror" : "Conqueror" ,
                "Gladiator" : "Gladiator" ,
                "Gryphon" : "Gryphon" ,
                "Highlander" : "Highlander" ,
                "Hitokiri" : "Hitokiri" ,
                "Jiang Jun" : "Jiang Jun" ,
                "Jormungandr" : "Jormungandr" ,
                "Kensei" : "Kensei" ,
                "Kyoshin" : "Kyoshin" ,
                "Lawbringer" : "Lawbringer" ,
                "Nobushi" : "Nobushi" ,
                "Nuxia" : "Nuxia" ,
                "Orochi" : "Orochi" ,
                "Peacekeeper" : "Peacekeeper" ,
                "Pirate" : "Pirate" ,
                "Raider" : "Raider" ,
                "Shaman" : "Shaman" ,
                "Shaolin" : "Shaolin" ,
                "Shinobi" : "Shinobi" ,
                "Shugoki" : "Shugoki" ,
                "Tiandi" : "Tiandi" ,
                "Valkyrie" : "Valkyrie" ,
                "Warden" : "Warden" ,
                "Warlord" : "Warlord" ,
                "Warmonger" : "Warmonger" ,
                "Zhanhu" : "Zhanhu",
                "Medjay" : "Medjay",
                "OutlandersH032Gazelle" : "Afeera",
                "Afeera" : "Afeera"
    }

modeNames = {
        "Dominion" : "Dominion" ,
        "Duel" : "Duel",
        "Breach" : "Breach",
        "Elimination" : "Elimination" ,
        "Skirmish" : "Skirmish",
        "Tribute" : "Tribute" ,
        "Ranked Duel" : "Ranked Duel",
    }

def constructUserCheckHashmap():
    userFile = open("usersTesting03-15-1.txt","r")
    usersFileLines = userFile.readlines()
    userFile.close()
    userCheckHashmap = {}
    # print()
    for line in usersFileLines:
        splitLine = line.split(",")
        platform = splitLine[0]
        username = splitLine[1][0:-1]
        splicedUsername = username.split("%20")
        splicedUsername = " ".join(splicedUsername)
        userCheckHashmap[f"{platform},{splicedUsername}"] = 1
        # print(f"\r{platform} : {username}",end="")
    return userCheckHashmap

# turns tet of the format 123321 into an integer
# why not return int("".join(text.split(','))) ?
def textToInt(text):
    splitText = text.split(',')
    splitText.reverse()
    num = 0
    for i in range(len(splitText)):
        num += int(splitText[i]) * (10**(i * 3))
    
    return num


# takes the text values of the overview page and returns a dict of these values
def parseOverview(username, platform, overviewTxt):
    overview = {}
    splitText = overviewTxt.split("\n")

    for i in range(len(splitText)):
        item = splitText[i]
        # play time
        if   re.match(r"^.* Play Time$", item):
            timeSplit = item.split(' ')
            timeInSeconds = 0
            for part in timeSplit:
                if re.match(r"^.*h$", part):
                    timeInSeconds += 3600 * textToInt(part[:-1])
                if re.match(r"^.*m$", part):
                    timeInSeconds += 60 * textToInt(part[:-1])
                if re.match(r"^.*s$", part):
                    timeInSeconds += 1 * textToInt(part[:-1])
            overview['time'] = timeInSeconds

        elif re.match(r"^Reputation.*$", item):
            repSplit = item.split(" ")
            overview['reputation'] = textToInt(repSplit[-1])
        elif re.match(r"^Wins$", item):
            overview['wins'] = textToInt(splitText[i+1])
        elif re.match(r"^Losses$", item):
            overview['losses'] = textToInt(splitText[i+1])
        elif re.match(r"^Kills \(Player\)$", item):
            overview['kills'] = textToInt(splitText[i+1])
        elif re.match(r"^Deaths$", item):
            overview['deaths'] = textToInt(splitText[i+1])
        elif re.match(r"^Assists$", item):
            overview['assists'] = textToInt(splitText[i+1])
    # username
    overview['username'] = username
    # platform
    overview['platform'] = platform
    # faction
    overview['faction'] = 0
    # UTCSeconds
    overview['date'] = time.time()

    return overview

# takes the text values of the heros page and returns a dict of these values
def parseHeros(herosTxt):
    splitText = herosTxt.split('\n')
    heroNames = {
                "Aramusha" : "Aramusha" ,
                "Berserker" : "Berserker" ,
                "Black Prior" : "Black Prior" ,
                "Centurion" : "Centurion"  ,
                "Conqueror" : "Conqueror" ,
                "Gladiator" : "Gladiator" ,
                "Gryphon" : "Gryphon" ,
                "Highlander" : "Highlander" ,
                "Hitokiri" : "Hitokiri" ,
                "Jiang Jun" : "Jiang Jun" ,
                "Jormungandr" : "Jormungandr" ,
                "Kensei" : "Kensei" ,
                "Kyoshin" : "Kyoshin" ,
                "Lawbringer" : "Lawbringer" ,
                "Nobushi" : "Nobushi" ,
                "Nuxia" : "Nuxia" ,
                "Orochi" : "Orochi" ,
                "Peacekeeper" : "Peacekeeper" ,
                "Pirate" : "Pirate" ,
                "Raider" : "Raider" ,
                "Shaman" : "Shaman" ,
                "Shaolin" : "Shaolin" ,
                "Shinobi" : "Shinobi" ,
                "Shugoki" : "Shugoki" ,
                "Tiandi" : "Tiandi" ,
                "Valkyrie" : "Valkyrie" ,
                "Warden" : "Warden" ,
                "Warlord" : "Warlord" ,
                "Warmonger" : "Warmonger" ,
                "Zhanhu" : "Zhanhu",
                "Medjay" : "Medjay",
                "OutlandersH032Gazelle" : "Afeera",
                "Afeera" : "Afeera"
    }
    heros = {}
    currentHero = ""
    done = False
    for i in range(len(splitText)):
        
        item = splitText[i]
        if item in heroNames:
            currentHero = heroNames[item]
            heros[currentHero] = {}
        else:
            if   re.match(r"^Time Played$", item):
                timeSplit = splitText[i+1].split(' ')
                timeInSeconds = 0
                for part in timeSplit:
                    if re.match(r"^.*h$", part):
                        timeInSeconds += 3600 * textToInt(part[:-1])
                    if re.match(r"^.*m$", part):
                        timeInSeconds += 60 * textToInt(part[:-1])
                    if re.match(r"^.*s$", part):
                        timeInSeconds += 1 * textToInt(part[:-1])
                if 'time' not in heros[currentHero]:
                    heros[currentHero]['time'] = timeInSeconds

            elif re.match(r"^Wins$", item):
                if 'wins' not in heros[currentHero]:
                    heros[currentHero]['wins'] = textToInt(splitText[i+1])
            elif re.match(r"^Losses$", item) and not done:
                if 'losses' not in heros[currentHero]:
                    heros[currentHero]['losses'] = textToInt(splitText[i+1])
            elif re.match(r"^Kills \(Player\)$", item):
                if 'kills' not in heros[currentHero]:
                    heros[currentHero]['kills'] = textToInt(splitText[i+1])
            elif re.match(r"^Deaths \(Player\)$", item):
                if 'deaths' not in heros[currentHero]:
                    heros[currentHero]['deaths'] = textToInt(splitText[i+1])
            elif re.match(r"^Assists \(Player\)$", item):
                if 'assists' not in heros[currentHero]:
                    heros[currentHero]['assists'] = textToInt(splitText[i+1])

    return heros

# takes the text values of the modes page and returns a dict of these values
# psn/woodcat102
def parseModes(modesTxt):
    splitText = modesTxt.split("\n")
    modeNames = {
        "Dominion" : "Dominion" ,
        "Duel" : "Duel",
        "Breach" : "Breach",
        "Elimination" : "Elimination" ,
        "Skirmish" : "Skirmish",
        "Tribute" : "Tribute" ,
        "Ranked Duel" : "Ranked Duel",
    }
    modes = {}
    currentMode = ""
    for i in range(len(splitText)):
        item = splitText[i]
        if item in modeNames:
            currentMode = item
            modes[currentMode] = {}
        else:
            if   re.match(r"^.* Play Time$", item):
                timeSplit = item.split(' ')
                timeInSeconds = 0
                for part in timeSplit:
                    if re.match(r"^.*h$", part):
                        timeInSeconds += 3600 * textToInt(part[:-1])
                    if re.match(r"^.*m$", part):
                        timeInSeconds += 60 * textToInt(part[:-1])
                    if re.match(r"^.*s$", part):
                        timeInSeconds += 1 * textToInt(part[:-1])
                
                if 'time' not in modes[currentMode]:
                    modes[currentMode]['time'] = timeInSeconds

            elif re.match(r"^Wins$", item):
                if 'wins' not in modes[currentMode]:
                    modes[currentMode]['wins'] = textToInt(splitText[i+1])
            elif re.match(r"^Losses$", item):
                if 'losses' not in modes[currentMode]:
                    modes[currentMode]['losses'] = textToInt(splitText[i+1])
            elif re.match(r"^Kills \(Player\)$", item):
                if 'kills' not in modes[currentMode]:
                    modes[currentMode]['kills'] = textToInt(splitText[i+1])
            elif re.match(r"^Deaths \(Player\)$", item):
                if 'deaths' not in modes[currentMode]:
                    modes[currentMode]['deaths'] = textToInt(splitText[i+1])
            elif re.match(r"^Assists \(Player\)$", item):
                if 'assists' not in modes[currentMode]:
                    modes[currentMode]['assists'] = textToInt(splitText[i+1])  

    return modes

