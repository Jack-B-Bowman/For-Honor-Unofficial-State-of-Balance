import sqlite3

from matplotlib.pyplot import pause
conn = sqlite3.connect("FH.db")
crsr = conn.cursor()

anomolies = []
day = 86400.0

def getStatByUsername(username,platform):
    sql = f"""SELECT * FROM stat WHERE username='{username}' and platform='{platform}' ORDER BY playerID"""
    crsr.execute(sql)
    ans = crsr.fetchall()
    if len(ans) > 1:
        if ans[0][1] == "b1.exe":
            print("pause")
        # sort by the playerID
        
        # check all adjacent entries
        for i in range(1,len(ans)):
            current = ans[i]
            previous = ans[i-1]
            deltaTime = current[4] - previous[4]
            deltaRep  = current[5] - previous[5]
            deltaK = current[6] - previous[6]
            deltaD = current[7] - previous[7]
            deltaA = current[8] - previous[8]
            deltaW = current[9] - previous[9]
            deltaL = current[10] - previous[10]
            deltaT = current[11] - previous[11]
            # if the difference in time is < 0 then all stats from the later should be smaller than the former      
            if deltaTime < 0:
                if any(x > y for x, y in zip(current[5:], previous[5:])):
                    anomolies.append((current[1], previous[0],"negative time stat anomoly",previous[4]))
            # if the difference in time is > 0 then all stats from the later should be larger than the former      
            elif deltaTime > 0:
                numDays = deltaTime / day 
                if any(x < y for x, y in zip(current[5:], previous[5:])):
                    anomolies.append((current[1], current[0],"positive time stat anomoly",previous[4]))
                elif numDays > 1:
                    if deltaRep / numDays > 15:
                        anomolies.append((current[1], current[0],f"{(deltaRep / numDays):.2f} per day rep gain stat anomoly", current[4]))
                    elif deltaK / numDays > 1000:
                        anomolies.append((current[1], current[0],f"{(deltaK / numDays):.2f} per day kill gain stat anomoly", current[4]))           
                    elif deltaD / numDays > 1000:
                        anomolies.append((current[1], current[0],f"{(deltaD / numDays):.2f} per day death gain stat anomoly", current[4]))  
                    elif deltaA / numDays > 3000:
                        anomolies.append((current[1], current[0],f"{(deltaA / numDays):.2f} per day assist gain stat anomoly", current[4]))  
                    elif deltaW / numDays > 300:
                        anomolies.append((current[1], current[0],f"{(deltaW / numDays):.2f} per day win gain stat anomoly", current[4]))  
                    elif deltaL / numDays > 300:
                        anomolies.append((current[1], current[0],f"{(deltaL / numDays):.2f} per day loss gain stat anomoly", current[4]))  
                    elif deltaT / numDays > day/2:
                        anomolies.append((current[1], current[0],f"{(deltaT / numDays):.2f} per day time gain stat anomoly", current[4]))  
getUsernames = """SELECT DISTINCT username,platform from stat"""
crsr.execute(getUsernames)
allUsernames = crsr.fetchall()
for username in allUsernames:
    getStatByUsername(username[0],username[1])

file = open("anomolies.txt","w")
for anomoly in anomolies:
    file.write(f"{anomoly[0]},{anomoly[1]},{anomoly[2]},{anomoly[3]}\n")
file.close()

# for anomoly in anomolies:
#     columnName = ""
#     value = ""
#     deleteFromMode = f"""delete from mode where {columnName}='{value}'"""
#     deleteFromHero = f"""delete from mode where {columnName}='{value}'"""
#     deleteFromStat = f"""delete from mode where {columnName}='{value}'"""
#     playerID = anomoly[1]
#     crsr.execute(f"""select playerID,username from stat where username='{anomoly[0]}'""")
#     ans = crsr.fetchall()
#     if len(ans) == 2:
#         crsr.execute(f"""delete from mode where playerID='{ans[0][0]}'""")
#         crsr.execute(f"""delete from mode where playerID='{ans[1][0]}'""")

#         crsr.execute(f"""delete from hero where playerID='{ans[0][0]}'""")
#         crsr.execute(f"""delete from hero where playerID='{ans[1][0]}'""")

#         crsr.execute(f"""delete from stat where username='{ans[0][1]}'""")
#     else:
#         columnName = "playerID"
#         value = playerID
#         deleteFromMode = f"""delete from mode where {columnName}='{value}'"""
#         deleteFromHero = f"""delete from hero where {columnName}='{value}'"""
#         deleteFromStat = f"""delete from stat where {columnName}='{value}'"""
#         crsr.execute(deleteFromMode)
#         crsr.execute(deleteFromHero)
#         crsr.execute(deleteFromStat)

# conn.commit()