import numpy as np
import sqlite3
conn = sqlite3.connect("FH.db")
crsr = conn.cursor()

# this script takes all the names in the failed users file and checks if they existed 
# at some point in the database. If this is the case they are added to the failed users table
# this table will be used to find players who have changed their name but still play the game

print("Reading failed users from file...")
file = open('C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\failedUsers.csv',"r")
fakeUsers = file.readlines()
file.close()

print("selecting all users from DB...")
# select all unique username+platform
sql = f"""select platform,username from stat group by username,platform"""
crsr.execute(sql)
ans = crsr.fetchall()

usersDict = {
    'xbl' : {},
    'psn' : {},
    'uplay' : {}
}

print("adding all users to dict")
# insert all database users into dict
for tup in ans:
    platform = tup[0]
    username = tup[1]
    usersDict[platform][username] = 1

# list of all players who existed at one point and have since renamed themselves
deadPlayers = []

print("adding dead players to list")
# for all failed users
for user in fakeUsers:
    splitUser = user.split(',')
    platform = splitUser[0]
    username = splitUser[1][:-1]

    if username in usersDict[platform]:
        deadPlayers.append((platform,username))

print("adding dead players list to DB")
print("inserting...")
crsr.execute('BEGIN TRANSACTION')
for user in deadPlayers:
    fields = "(platform,username)"
    values = f"('{user[0]}','{user[1]}')"
    sql = (f"INSERT INTO failedUsers "
                f"{fields} "
                f"VALUES {values};\n"
                )
                
    # print(sql)
    try:
        crsr.execute(sql)
    except:
        ...
print()


conn.commit()
conn.close()
