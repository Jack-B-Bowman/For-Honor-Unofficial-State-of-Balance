import json
import time
import random
import sys
import threading
import sqlite3
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
mutex = threading.Lock()

arg = 0
if len(sys.argv) < 2:
    arg = 1
else: arg = int(sys.argv[1])

# read in the users csv
userFile = open("compiledUsers-06-27-1.csv","r")
usersFileLines = userFile.readlines()
userFile.close()
users = []

for line in usersFileLines:
    splitLine = line.split(",")
    platform = splitLine[0]
    username = splitLine[1][0:-1]
    splicedUsername = username.split("%20")
    splicedUsername = " ".join(splicedUsername)
    users.append((platform,username))


# shuffle the list for random selection from users
random.shuffle(users)


id = 0


nonExistantUsersFile = open(".\\failedUsers.csv","r")
nonExistantUsersList = nonExistantUsersFile.readlines()
failedUsersDict = {}
for user in nonExistantUsersList:
    failedUsersDict[user] = True

def checkIntegrety(username,platform,data):
    if data['platformInfo']['platformUserHandle'] != username:
        return False
    if data['platformInfo']['platformSlug'] != platform:
        return False
    return True

def downloadThread(id):
    conn = sqlite3.connect("FH.db")
    crsr = conn.cursor()
    players = {}
    data = {}
    opts = uc.ChromeOptions()
    # opts.headless = True
    # opts.add_argument('--headless')
    # opts.add_argument('--proxy-server=103.147.118.17:9091')
    opts.add_argument("--window-size=1020,900")  
    # opts.add_argument("--unsafe-pac-url")  

    driver = uc.Chrome(options=opts, use_subprocess=True)
    # time.sleep(60)
    num = 0
    while len(users) > 0:
        time.sleep(2)
        mutex.acquire()
        user = users.pop()
        mutex.release()

        skipUser = False
        timeForUpdate = False
        platform = user[0]
        username = user[1]

        splitUsername = username.split("%20")
        fortmattedUN = " ".join(splitUsername)
        

        sql = f"""SELECT username,platform,UTCSeconds from stat where username='{fortmattedUN}' and platform='{platform}'"""
        crsr.execute(sql)
        ans = crsr.fetchall()
        ans.sort(key=lambda y:y[2])
        # if the player exists
        timeForUpdate = False
        # does the player exist
        if len(ans) > 0: 
            # is the player inactive
            if len(ans) == 1:
                # if the player exists and is inactive update them once every 2 weeks
                if(time.time() - ans[-1][2] > (86400 * 14)):
                    timeForUpdate = True
            else:
                timeBetweenUpdates = ans[-1][2] - ans[-2][2]
                # if the player has not played in a month update them once a week
                if timeBetweenUpdates > 86400 * 30:
                    if(time.time() - ans[-1][2] > (86400 * 7)):
                        timeForUpdate = True
                # if the player has played in the last 30 days update them once a day
                else:
                    if(time.time() - ans[-1][2] > (86400 * 1)):
                        timeForUpdate = True
        if len(ans) == 0:
            timeForUpdate = True

        lineString = user[0] + "," + fortmattedUN + "\n"

        url = ""
        html_data = ""
        if lineString not in failedUsersDict and timeForUpdate:
            # catches any errors and skips the user if they gave an error. (this section would throw an error every thousand users or so)
            try:
                # url = f'http://api.tracker.gg/api/v2/for-honor/standard/profile/{platform}/{username}?{num % 10}'
                url = f'https://tracker.gg/for-honor/profile/{platform}/{username}/pvp'
                print(url)
                driver.get(url)
                num += 1
                # pre = driver.find_element(by=By.TAG_NAME,value="pre").text
                # print(pre)
                # html_data = json.loads(pre)
                # if 'errors' in html_data:
                #     mutex.acquire()
                #     failedUsersFile = open(".\\failedUsers.csv","a")
                #     failedUsersFile.write(platform + "," + username + "\n")
                #     failedUsersFile.close()
                #     mutex.release()
                # else:
                    # data = html_data['data']
                    # splitUsername = username.split("%20")
                    # TempUsername = " ".join(splitUsername)
                    # assert checkIntegrety(TempUsername,platform,data)

            except Exception as e:
                print("GET error:\n", e)
                # failedUsersFile = open("failedUsers.csv","a")
                # failedUsersFile.write(platform + "," + username + "," + str(e))
                # failedUsersFile.close()
                skipUser = True
                # time.sleep(300)
        else:
            skipUser = True
        


        # the stat tracker replaces spaces in the url with "%20" but the initial state json uses spaces when referencing the username
        # this simply reconstructs the actual username


    dataFile = open(f".\\datafiles\\dataFinal-{id}.json","a")
    dataFile.write(json.dumps(players))
    dataFile.close()
    players = {}

number = len(users)

threads = []
for n in range(arg):
    t = threading.Thread(target=downloadThread, args=[n])
    t.start()
    threads.append(t)
    time.sleep(180)

for item in threads:
    item.join()





