import json
import time
import random
import sys
import threading
import sqlite3
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
import re
from CommonSeleniumScraperFunctions import * 
mutex = threading.Lock()

"""
! 2022-12-19 https://tracker.gg
tracker.gg##.overlay
tracker.gg##.warden-challenge.container
tracker.gg##body:style(overflow:auto!important)

||tracker.gg/sw.js$script,1p,important

! 2022-12-19 https://newassets.hcaptcha.com
||newassets.hcaptcha.com/c/b4b4ffc/hsw.js$script,domain=newassets.hcaptcha.com
||newassets.hcaptcha.com/i/b4b4ffc/e$xhr,domain=newassets.hcaptcha.com
||hcaptcha.com/checksiteconfig?v=220a550&host=tracker.gg&sitekey=719e6c36-9055-4bc9-b01f-720bceda362e&sc=1&swa=1$xhr,domain=newassets.hcaptcha.com

! 2022-12-19 https://tracker.gg
||newassets.hcaptcha.com/captcha/v1/220a550/static/hcaptcha.html$subdocument,domain=tracker.gg

"""


arg = 0
if len(sys.argv) < 2:
    arg = 1
else: arg = int(sys.argv[1])

# read in the users csv
userFile = open("compiledUsers-12-04-1.csv","r")
usersFileLines = userFile.readlines()
userFile.close()
users = []
threads = []
threadData = {}

xpaths = {
    "overview" : "/html/body/div/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div/div[1]",
    "heroes" : "/html/body/div/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div",
    "modes" : "/html/body/div/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div",
    "heroesFactionDropdown" : "/html/body/div/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div/div[1]/div[2]/div",
}

file = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\downloadSchedule\\DownloadedNames.json","r")
downloadSchedule = json.load(file)
file.close()

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

def progThread(id):
    totalUsers = len(users)
    while(len(users) > 0):

        display = ""

        progress = 100 - ((len(users) / totalUsers) * 100)

        for thread in threadData:
            display += f"{thread} : ΔT = {threadData[thread]['time']:.2f} \t"

        display += f"{progress:.2f}%"
        print(f"\r{display}",end="")
        time.sleep(1)



def downloadThread(id):
    conn = sqlite3.connect("FH.db")
    crsr = conn.cursor()
    players = {}
    data = {}
    opts = uc.ChromeOptions()
    
    # opts.headless = True
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # opts.add_experimental_option("prefs", prefs)
    # opts.add_argument('--headless')
    # opts.add_argument('--proxy-server=103.147.118.17:9091')
    opts.add_argument("--window-size=1020,900")  
    opts.add_argument('--no-first-run --no-service-autorun --password-store=basic --no-default-browser-check')
    # opts.add_argument("--unsafe-pac-url")  
    # uc.TARGET_VERSION  = 104
    # driver = uc.Chrome(options=opts, use_subprocess=True, driver_executable_path = "C:\\\Program Files\\\Google\\\Chrome\\Application\\new_chrome.exe")
    driver = uc.Chrome(options=opts,driver_executable_path = "C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\chromedriver.exe")
    # driver = uc.Chrome(options=opts)
    driver.get("https://chrome.google.com/webstore/detail/ublock-origin/cjpalhdlnbpafiamejdnhcphjbkeiagm?hl=en")
    time.sleep(10)
    num = 0

    userCheckHashmap=constructUserCheckHashmap()

    while len(users) > 0:
        mutex.acquire()
        user = users.pop(0)
        mutex.release()

        skipUser = False
        timeForUpdate = False
        platform = user[0]
        username = user[1]
 
        splitUsername = username.split("%20")
        fortmattedUN = " ".join(splitUsername)
        

        if fortmattedUN + "," + platform in downloadSchedule:
            if time.time() > downloadSchedule[fortmattedUN + "," + platform]:
                timeForUpdate = True
            else:
                timeForUpdate = False
        else:
            timeForUpdate = True

        lineString = user[0] + "," + fortmattedUN + "\n"

        url = ""
        html_data = ""

        if lineString not in failedUsersDict and timeForUpdate:
            playerStartTime = time.time()
            try:
                # url = f'https://api.tracker.gg/api/v2/for-honor/standard/profile/{platform}/{username}?{num % 10}'
                # platform = "xbl"
                # username = "aqaurium"
                url = f'https://tracker.gg/for-honor/profile/{platform}/{username}/pvp'
                # print(url)
                driver.get(url)
                time.sleep(0.5)
                # print("get-time -> {time.time() - playerStartTime}")
                # driver.execute_script("document.getElementsByTagName(arguments[0])[0].className = arguments[1]","body","")
                # print("Overview")
                overview = "" 
                success = False
                startTime = time.time()
                # retry loop to avoid using sleeps
                while not success and time.time() - startTime < 10:
                    # driver.execute_script("document.getElementsByTagName(arguments[0])[0].className = arguments[1]","body","")
                    try:
                        overview = driver.find_element(by=By.CLASS_NAME,value="segment-stats.card.bordered.header-bordered.responsive").text
                        success = True
                    except:
                        try:
                            # handles non existant users
                            if driver.find_element(by=By.TAG_NAME,value="h1").text == "404":
                                raise Exception("404 Error")
                        except Exception as e:
                            if e.message == "404 Error":
                                raise Exception("404 Error")

                if not success:
                    raise Exception("Could not find overview elements in alloted time")

                # print("Tabs")
                tabs = ""
                success = False
                startTime = time.time()
                # retry loop to avoid using sleeps
                while not success and time.time() - startTime < 3:
                    # driver.execute_script("document.getElementsByTagName(arguments[0])[0].className = arguments[1]","body","")
                    try:
                        tabs = driver.find_elements(by=By.CLASS_NAME,value="trn-tabs__item")
                        success = True
                    except:
                        ...
                if not success:
                    raise Exception("Could not find tab elements in alloted time")

                tabs[1].click()
                # print("Heros")
                heros = ""
                success = False
                startTime = time.time()
                # retry loop to avoid using sleeps
                while not success and time.time() - startTime < 3:
                    # driver.execute_script("document.getElementsByTagName(arguments[0])[0].className = arguments[1]","body","")
                    try:
                        heros = driver.find_element(by=By.CLASS_NAME,value="trn-grid.trn-grid--small.heroes").text
                        success = True
                    except:
                        ...
                if not success:
                    raise Exception("Could not find hero data in alloted time")
                

                tabs[2].click()
                heroTabLoaded = True
                while heroTabLoaded and time.time() - startTime < 3:
                    # driver.execute_script("document.getElementsByTagName(arguments[0])[0].className = arguments[1]","body","")
                    try:
                        heros = driver.find_element(by=By.CLASS_NAME,value="trn-grid.trn-grid--small.heroes").text
                        heroTabLoaded = True
                    except:
                        heroTabLoaded = False
                # print("Modes")
                modes = ""
                success = False
                startTime = time.time()
                # retry loop to avoid using sleeps
                while not success and time.time() - startTime < 3:
                    try:
                        modes = driver.find_element(by=By.CLASS_NAME,value="trn-grid.trn-grid--small").text
                        success = True
                    except:
                        ...
                if not success:
                    raise Exception("Could not find mode data in alloted time")
                
                # print("Begin Proccessing...")

                splitUsername = username.split("%20")
                FormattedUsername = " ".join(splitUsername)

                players[FormattedUsername] = {
                "psn" : [],
                "xbl" : [],
                "uplay" : []
                }

                pretime = time.time()
                # print("Parse Overview")
                overviewData = parseOverview(username=FormattedUsername,platform=platform,overviewTxt=overview)
                # print("Parse Modes")
                try:
                    overviewData['modes'] = parseModes(modes)
                except:
                    overviewData['modes'] = parseModes(modes)
                # print("Parse Heros")
                overviewData['heros'] = parseHeros(heros)
                posttime = time.time()
                print(f"processing time = {posttime - pretime}")

                # print("Add Player To Dict")
                players[FormattedUsername][platform].append(overviewData)
                posttime = time.time()
                deltaT = posttime - playerStartTime
                mutex.acquire()
                threadData[str(id)]["time"] = deltaT
                mutex.release()
                num += 1
                # print(players[FormattedUsername])
                # print(f"ThreadID : {id}\n  count : {str(num)} \n  user : {FormattedUsername}") # current user

                if(num % 50 == 0):

                    dataFile = open(f".\\datafiles\\data{str(id)}-{str(num)}.json","a")
                    dataFile.write(json.dumps(players))
                    dataFile.close() 
                    # time.sleep(60)
                    players = {}


                


            except Exception as e:
                # print()
                # print(e)
                # print(fortmattedUN,platform)
                try:
                    try:
                        # handles non existant users
                        if driver.find_element(by=By.TAG_NAME,value="h1").text == "404":
                            
                            splitUsername = username.split("%20")
                            FormattedUsername = " ".join(splitUsername)

                            if(f"{platform},{FormattedUsername}" not in userCheckHashmap):
                                print("Oopsie I made a Fucky Wucky")

                            mutex.acquire()
                            failedUsersFile = open("failedUsers.csv","a")
                            failedUsersFile.write(platform + "," + FormattedUsername + "\n")
                            failedUsersFile.close()
                            mutex.release()
                            time.sleep(1)
                    except:
                        # handles players who have not played PVP
                        if driver.find_element(by=By.TAG_NAME,value="p").text == "Player has not played pvp.":
                            time.sleep(1)
                except:
                    # handles errors raised due to browser check   
                    print("GET error:\n", e)
                    mutex.acquire()
                    users.append((platform,username))
                    mutex.release()
                    time.sleep(5)
            
            endTime = time.time()
            # print(f"T = {(endTime - playerStartTime):.2f}")
            if(endTime - playerStartTime < 1):
                mutex.acquire()
                users.append((platform,username))
                mutex.release()
                time.sleep(5)
                

        


    dataFile = open(f".\\datafiles\\dataFinal-{id}.json","a")
    dataFile.write(json.dumps(players))
    dataFile.close()
    players = {}

number = len(users)

for n in range(arg):
    threadData[f"{n}"] = {
        "time" : 0,
        "stage": "",
        "count": ""
    }

gui = threading.Thread(target=progThread, args=[99])
gui.start()
threads.append(gui)
for n in range(arg):
    t = threading.Thread(target=downloadThread, args=[n])
    t.start()
    threads.append(t)
    time.sleep(2)

for item in threads:
    item.join()




