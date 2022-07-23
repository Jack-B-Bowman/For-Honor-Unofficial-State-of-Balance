import time
import re

def textToInt(text):
    splitText = text.split(',')
    splitText.reverse()
    num = 0
    for i in range(len(splitText)):
        num += int(splitText[i]) * (10**(i * 3))
    
    return num


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
    overview['UTCSeconds'] = time.time()

    return overview

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
                "SamuraiH029Faceless" : "Kyoshin" ,
                "Lawbringer" : "Lawbringer" ,
                "Nobushi" : "Nobushi" ,
                "Nuxia" : "Nuxia" ,
                "Orochi" : "Orochi" ,
                "Peacekeeper" : "Peacekeeper" ,
                "OutlandersH030PirateQueen" : "Pirate" ,
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
                "Zhanhu" : "Zhanhu"
    }
    heros = {}
    currentHero = ""
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
                heros[currentHero]['time'] = timeInSeconds

            elif re.match(r"^Wins$", item):
                heros[currentHero]['wins'] = textToInt(splitText[i+1])
            elif re.match(r"^Losses$", item):
                heros[currentHero]['losses'] = textToInt(splitText[i+1])
            elif re.match(r"^Kills \(Player\)$", item):
                heros[currentHero]['kills'] = textToInt(splitText[i+1])
            elif re.match(r"^Deaths \(Player\)$", item):
                heros[currentHero]['deaths'] = textToInt(splitText[i+1])
            elif re.match(r"^Assists \(Player\)$", item):
                heros[currentHero]['assists'] = textToInt(splitText[i+1])

    return heros

def parseModes(modesTxt):
    splitText = modesTxt.split("\n")
    modeNames = {
        "Dominion" : "Dominion" ,
        "Duel" : "Duel",
        "Breach" : "Breach",
        "Elimination" : "Elimination" ,
        "Skirmish" : "Skirmish"
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
                modes[currentMode]['time'] = timeInSeconds

            elif re.match(r"^Wins$", item):
                modes[currentMode]['wins'] = textToInt(splitText[i+1])
            elif re.match(r"^Losses$", item):
                modes[currentMode]['losses'] = textToInt(splitText[i+1])
            elif re.match(r"^Kills \(Player\)$", item):
                modes[currentMode]['kills'] = textToInt(splitText[i+1])
            elif re.match(r"^Deaths \(Player\)$", item):
                modes[currentMode]['deaths'] = textToInt(splitText[i+1])
            elif re.match(r"^Assists \(Player\)$", item):
                modes[currentMode]['assists'] = textToInt(splitText[i+1])  

    return modes

overviewTxt = """Player vs. Player Overview
49h Play Time
529 Matches
Reputation 11
Win %
47.8%
Bottom 13%
Wins
253
Top 32%
K/D Ratio (Player)
0.65
Bottom 45%
Kills (Player)
1,139
Top 29%
Losses
276
Top 26%
Ties
0
Deaths
1,777
Top 28%
Assists
427
Top 37%
Kills/min (Player)
0.38
Top 43%
Kills/match (Player)
2.15
Top 44%"""

print(parseOverview("test","test2",overviewTxt))

herosTxt = """https://tracker.gg/for-honor/profile/xbl/THE%20BATMAN%201407/pvp
Kill Type
Player
Faction
Class
Sort By
Win %
Peacekeeper
Assassins
Time Played
09m 45s
Matches Played
1
Win %
100.0%
Wins
1
Losses
0
Ties
0
Reputation
0
Level
3
K/D Ratio (Player)
0.33
KAD Ratio (Player)
1.50
Kills (Player)
2
Deaths (Player)
6
Assists (Player)
7
Kills/match (Player)
2.00
Kills/min (Player)
0.21
OutlandersH030PirateQueen
Time Played
23m 46s
Matches Played
2
Win %
100.0%
Wins
2
Losses
0
Ties
0
K/D Ratio (Player)
2.25
KAD Ratio (Player)
4.00
Kills (Player)
9
Deaths (Player)
4
Assists (Player)
7
Kills/match (Player)
4.50
Kills/min (Player)
0.38
SamuraiH029Faceless
Time Played
5h 55m
Matches Played
54
Win %
75.9%
Wins
41
Losses
13
Ties
0
K/D Ratio (Player)
1.51
KAD Ratio (Player)
1.99
Kills (Player)
229
Deaths (Player)
152
Assists (Player)
74
Kills/match (Player)
4.24
Kills/min (Player)
0.65
Gryphon
Hybrids
Time Played
20m 05s
Matches Played
3
Win %
66.7%
Wins
2
Losses
1
Ties
0
K/D Ratio (Player)
1.10
KAD Ratio (Player)
1.80
Kills (Player)
11
Deaths (Player)
10
Assists (Player)
7
Kills/match (Player)
3.67
Kills/min (Player)
0.55
Lawbringer
Hybrids
Time Played
3h 53m
Matches Played
37
Win %
64.9%
Wins
24
Losses
13
Ties
0
Reputation
0
Level
17
K/D Ratio (Player)
0.82
KAD Ratio (Player)
1.26
Kills (Player)
97
Deaths (Player)
119
Assists (Player)
53
Kills/match (Player)
2.62
Kills/min (Player)
0.41
Warden
Vanguards
Time Played
96h
Matches Played
1,081
Win %
57.1%
Wins
616
Losses
464
Ties
1
Reputation
17
Level
14
K/D Ratio (Player)
1.26
KAD Ratio (Player)
1.53
Kills (Player)
3,574
Deaths (Player)
2,832
Assists (Player)
745
Kills/match (Player)
3.31
Kills/min (Player)
0.62
Raider
Vanguards
Time Played
22h
Matches Played
194
Win %
56.2%
Wins
108
Losses
85
Ties
1
Reputation
4
Level
12
K/D Ratio (Player)
1.13
KAD Ratio (Player)
1.55
Kills (Player)
672
Deaths (Player)
597
Assists (Player)
256
Kills/match (Player)
3.46
Kills/min (Player)
0.51
Kensei
Vanguards
Time Played
8h 34m
Matches Played
69
Win %
53.6%
Wins
37
Losses
32
Ties
0
Reputation
2
Level
6
K/D Ratio (Player)
1.14
KAD Ratio (Player)
1.64
Kills (Player)
287
Deaths (Player)
251
Assists (Player)
124
Kills/match (Player)
4.16
Kills/min (Player)
0.56
Warlord
Heavies
Time Played
6h 54m
Matches Played
57
Win %
52.6%
Wins
30
Losses
27
Ties
0
Reputation
1
Level
16
K/D Ratio (Player)
1.00
KAD Ratio (Player)
1.41
Kills (Player)
209
Deaths (Player)
208
Assists (Player)
85
Kills/match (Player)
3.67
Kills/min (Player)
0.50
Tiandi
Hybrids
Time Played
6h 01m
Matches Played
45
Win %
51.1%
Wins
23
Losses
22
Ties
0
K/D Ratio (Player)
0.85
KAD Ratio (Player)
1.27
Kills (Player)
163
Deaths (Player)
192
Assists (Player)
80
Kills/match (Player)
3.62
Kills/min (Player)
0.45
Shugoki
Heavies
Time Played
19m 28s
Matches Played
2
Win %
50.0%
Wins
1
Losses
1
Ties
0
Reputation
0
Level
4
K/D Ratio (Player)
0.29
KAD Ratio (Player)
0.79
Kills (Player)
4
Deaths (Player)
14
Assists (Player)
7
Kills/match (Player)
2.00
Kills/min (Player)
0.21
Jormungandr
Heavies
Time Played
1h 48m
Matches Played
13
Win %
46.1%
Wins
6
Losses
7
Ties
0
K/D Ratio (Player)
1.12
KAD Ratio (Player)
1.51
Kills (Player)
46
Deaths (Player)
41
Assists (Player)
16
Kills/match (Player)
3.54
Kills/min (Player)
0.42
Black Prior
Hybrids
Time Played
3h 30m
Matches Played
27
Win %
44.4%
Wins
12
Losses
15
Ties
0
K/D Ratio (Player)
0.78
KAD Ratio (Player)
1.17
Kills (Player)
74
Deaths (Player)
95
Assists (Player)
37
Kills/match (Player)
2.74
Kills/min (Player)
0.35
Jiang Jun
Hybrids
Time Played
4h 46m
Matches Played
35
Win %
42.9%
Wins
15
Losses
20
Ties
0
K/D Ratio (Player)
1.03
KAD Ratio (Player)
1.53
Kills (Player)
149
Deaths (Player)
144
Assists (Player)
71
Kills/match (Player)
4.26
Kills/min (Player)
0.52
Zhanhu
Hybrids
Time Played
2h 29m
Matches Played
14
Win %
42.9%
Wins
6
Losses
8
Ties
0
K/D Ratio (Player)
1.01
KAD Ratio (Player)
1.28
Kills (Player)
76
Deaths (Player)
75
Assists (Player)
20
Kills/match (Player)
5.43
Kills/min (Player)
0.51
Conqueror
Heavies
Time Played
23h
Matches Played
221
Win %
41.2%
Wins
91
Losses
130
Ties
0
Reputation
3
Level
17
K/D Ratio (Player)
0.69
KAD Ratio (Player)
0.99
Kills (Player)
519
Deaths (Player)
749
Assists (Player)
220
Kills/match (Player)
2.35
Kills/min (Player)
0.36
Centurion
Hybrids
Time Played
26h
Matches Played
227
Win %
40.5%
Wins
92
Losses
135
Ties
0
K/D Ratio (Player)
0.87
KAD Ratio (Player)
1.16
Kills (Player)
719
Deaths (Player)
831
Assists (Player)
245
Kills/match (Player)
3.17
Kills/min (Player)
0.45
Orochi
Assassins
Time Played
50m 50s
Matches Played
5
Win %
40.0%
Wins
2
Losses
3
Ties
0
Reputation
0
Level
7
K/D Ratio (Player)
0.32
KAD Ratio (Player)
0.64
Kills (Player)
9
Deaths (Player)
28
Assists (Player)
9
Kills/match (Player)
1.80
Kills/min (Player)
0.18
Gladiator
Assassins
Time Played
3h 07m
Matches Played
31
Win %
38.7%
Wins
12
Losses
19
Ties
0
K/D Ratio (Player)
0.69
KAD Ratio (Player)
0.85
Kills (Player)
79
Deaths (Player)
114
Assists (Player)
18
Kills/match (Player)
2.55
Kills/min (Player)
0.42
Shinobi
Hybrids
Time Played
1h 57m
Matches Played
12
Win %
33.3%
Wins
4
Losses
8
Ties
0
K/D Ratio (Player)
0.49
KAD Ratio (Player)
0.93
Kills (Player)
34
Deaths (Player)
70
Assists (Player)
31
Kills/match (Player)
2.83
Kills/min (Player)
0.29
Berserker
Assassins
Time Played
2h 35m
Matches Played
21
Win %
28.6%
Wins
6
Losses
15
Ties
0
Reputation
0
Level
14
K/D Ratio (Player)
0.67
KAD Ratio (Player)
0.98
Kills (Player)
63
Deaths (Player)
94
Assists (Player)
29
Kills/match (Player)
3.00
Kills/min (Player)
0.40
Shaolin
Hybrids
Time Played
1h 11m
Matches Played
7
Win %
28.6%
Wins
2
Losses
5
Ties
0
K/D Ratio (Player)
0.41
KAD Ratio (Player)
0.93
Kills (Player)
17
Deaths (Player)
41
Assists (Player)
21
Kills/match (Player)
2.43
Kills/min (Player)
0.24
Highlander
Hybrids
Time Played
28m 42s
Matches Played
4
Win %
25.0%
Wins
1
Losses
3
Ties
0
K/D Ratio (Player)
0.63
KAD Ratio (Player)
1.05
Kills (Player)
12
Deaths (Player)
19
Assists (Player)
8
Kills/match (Player)
3.00
Kills/min (Player)
0.42
Valkyrie
Hybrids
Time Played
15m 53s
Matches Played
1
Win %
0.0%
Wins
0
Losses
1
Ties
0
Reputation
0
Level
2
K/D Ratio (Player)
0.33
KAD Ratio (Player)
1.00
Kills (Player)
1
Deaths (Player)
3
Assists (Player)
2
Kills/match (Player)
1.00
Kills/min (Player)
0.06
Hitokiri
Hybrids
Time Played
06m 52s
Matches Played
1
Win %
0.0%
Wins
0
Losses
1
Ties
0
K/D Ratio (Player)
0.00
KAD Ratio (Player)
0.00
Kills (Player)
0
Deaths (Player)
3
Assists (Player)
0
Kills/match (Player)
0.00
Kills/min (Player)
0.00"""

print(parseHeros(herosTxt))

modesText = """https://tracker.gg/for-honor/profile/xbl/KirbyMerc/pvp
Player vs. Player
Player vs. A.I.
Kill Type
Player
Dominion
79h Play Time
529 Matches
K/D Ratio (Player)
0.92
Kills (Player)
2,178
Deaths (Player)
2,373
Assists (Player)
1,120
Kills/match (Player)
4.12
Kills/min (Player)
0.46
Win %
48.4%
Wins
256
Losses
273
Ties
0
Duel
54m 54s Play Time
14 Matches
K/D Ratio (Player)
0.79
Kills (Player)
27
Deaths (Player)
34
Assists (Player)
1
Kills/match (Player)
1.93
Kills/min (Player)
0.49
Win %
42.9%
Wins
6
Losses
8
Ties
0
Breach
3h 09m Play Time
8 Matches
K/D Ratio (Player)
0.93
Kills (Player)
83
Deaths (Player)
89
Assists (Player)
45
Kills/match (Player)
10.38
Kills/min (Player)
0.44
Win %
12.5%
Wins
1
Losses
7
Ties
0
Obj. Score
6,985
Obj. Score/match
873
Obj. Score/min
37
Ranked Duel
03m 53s Play Time
1 Matches
K/D Ratio (Player)
0.33
Kills (Player)
1
Deaths (Player)
3
Assists (Player)
0
Kills/match (Player)
1.00
Kills/min (Player)
0.26
Win %
0.0%
Wins
0
Losses
1
Ties
0
Premium users don't see ads.
Upgrade for $3/mo"""

print(parseModes(modesText))