import json
import time
import random
import sys
import threading
import sqlite3
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from CommonSeleniumScraperFunctions import *
import re
mutex = threading.Lock()

ublockSettings = """
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
    arg = 4
else: arg = int(sys.argv[1])

# read in the users csv
userFile = open("compiledUsers-12-04-1.csv","r")
usersFileLines = userFile.readlines()
userFile.close()
users = []
threads = []
threadData = {}

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

xpaths = {
    "overview" : "/html/body/div/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div/div[1]",
    "heroes" : "/html/body/div/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div",
    "modes" : "/html/body/div/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div",
    "heroesFactionDropdown" : "/html/body/div/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div/div[1]/div[2]/div",
}

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

def handle404(driver,platform,formattedUsername,userCheckHashmap):
    try:
        # handles non existant users
        if driver.find_element(by=By.TAG_NAME,value="h1").text == "404":

            if(f"{platform},{formattedUsername}" not in userCheckHashmap):
                print("Oopsie I made a Fucky Wucky")

            mutex.acquire()
            failedUsersFile = open("failedUsers.csv","a")
            failedUsersFile.write(platform + "," + formattedUsername + "\n")
            failedUsersFile.close()
            mutex.release()
            # time.sleep(1)
    except:
        # handles players who have not played PVP
        if driver.find_element(by=By.TAG_NAME,value="p").text == "Player has not played pvp.":
            time.sleep(1)

def waitOnElementByXpath(driver,waitTime,xPath):
    elementExists = False
    try:
        tabs = WebDriverWait(driver, timeout=waitTime).until(lambda d: d.find_elements(by=By.XPATH,value=xPath))
        elementExists = True
    except:
        return elementExists
    return elementExists

def waitOnElement(driver,waitTime,classText):
    elementExists = False
    try:
        tabs = WebDriverWait(driver, timeout=waitTime).until(lambda d: d.find_elements(by=By.CLASS_NAME,value=classText))
        elementExists = True
    except:
        return elementExists
    return elementExists

def getElementsByClass(driver,classText,waitTime=0):
    elementsList = []
    try:
        elementsList = WebDriverWait(driver, timeout=waitTime).until(lambda d: d.find_elements(by=By.CLASS_NAME,value=classText))
    except:
        ...
    return elementsList

def getElementByXpath(driver,xpath,waitTime=0):
    element = ""
    try:
        element = WebDriverWait(driver, timeout=waitTime).until(lambda d: d.find_element(by=By.XPATH,value=xpath))
    except:
        ...
    return element

def getElementByCSS(driver,CSS,waitTime=0):
    element = ""
    try:
        element = WebDriverWait(driver, timeout=waitTime).until(lambda d: d.find_element(by=By.CSS_SELECTOR,value=CSS))
    except:
        ...
    return element

def getURL(driver,url):
        driver.get(url)
        try:
            WebDriverWait(driver,10).until(EC.any_of(
            EC.presence_of_element_located((By.CLASS_NAME,"content--error")),
            EC.presence_of_element_located((By.CLASS_NAME,"trn-ign__username")),
            EC.presence_of_element_located((By.CLASS_NAME,"captcha-prompt"))))
        except:
            getURL(driver,url)

def downloadThread(id):
    players = {}
    opts = uc.ChromeOptions()
    
    # opts.headless = True
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # opts.add_experimental_option("prefs", prefs)
    # opts.add_argument('--headless')
    # opts.add_argument('--proxy-server=103.147.118.17:9091')
    opts.add_argument("--window-size=1020,900")  
    opts.add_argument('--no-first-run --no-service-autorun --password-store=basic --no-default-browser-check')
    opts.add_argument("--load-extension=C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\extensions\\extension_1_45_2_0")
    # opts.add_extension("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\extensions\\extension_1_45_2_0.crx")
    # opts.add_argument("--unsafe-pac-url")  
    # uc.TARGET_VERSION  = 104
    # driver = uc.Chrome(options=opts, use_subprocess=True, driver_executable_path = "C:\\\Program Files\\\Google\\\Chrome\\Application\\new_chrome.exe")
    driver = uc.Chrome(options=opts,driver_executable_path = "C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\chromedriver.exe")
    # driver.implicitly_wait(10)
    # driver = uc.Chrome(options=opts)
    # driver.get("https://chrome.google.com/webstore/detail/ublock-origin/cjpalhdlnbpafiamejdnhcphjbkeiagm?hl=en")
    # installBtn = getElements(driver,"g-c-Hf",waitTime=5)
    # installBtn[0].click()
    time.sleep(1)
    driver.get("chrome-extension://cjpalhdlnbpafiamejdnhcphjbkeiagm/dashboard.html#1p-filters.html")
    time.sleep(1)
    UblockTabs = getElementsByClass(driver,"tabButton",5)
    UblockTabs[2].click()
    frame =  WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(by=By.ID,value="iframe"))
    driver.switch_to.frame(frame)
    lines = getElementsByClass(driver,"CodeMirror-line",5)
    # add ublock settings
    # driver.execute_script("document.evaluate('/html/body/div[2]/div/div[2]/div[6]/div[1]/div/div/div/div[5]/div[1]/pre/span/span', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.innerHTML=arguments[0];",ublockSettings)
    # enable button
    # driver.execute_script("document.evaluate('/html/body/div[1]/p[2]/button[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.disabled=false;")
    # Alert(driver).accept()
    # time.sleep(10)
    num = 0

    userCheckHashmap=constructUserCheckHashmap()

    while len(users) > 0:

        mutex.acquire()
        user = users.pop(0)
        mutex.release()

        timeForUpdate = False
        platform = user[0]
        username = user[1]
        try:   
            splitUsername = username.split("%20")
            fortmattedUN = " ".join(splitUsername)
            
            if fortmattedUN not in downloadSchedule:
                timeForUpdate = True
            elif time.time() > downloadSchedule[fortmattedUN + "," + platform]:
                timeForUpdate = True
            else:
                timeForUpdate = False


            lineString = user[0] + "," + fortmattedUN + "\n"

            if lineString not in failedUsersDict and timeForUpdate:
                
                playerStartTime = time.time()
                # get page
                url = f'https://tracker.gg/for-honor/profile/{platform}/{username}/pvp'
                driver.get(url)
                # print(url)
        
                tabs = []
                # wait for 404 or tabs to show
                driver.find_elements(By.CLASS_NAME,"trn-ign__username")

                try:
                    WebDriverWait(driver,10).until(EC.any_of(
                    EC.presence_of_element_located((By.CLASS_NAME,"content--error")),
                    EC.presence_of_element_located((By.CLASS_NAME,"trn-ign__username")),
                    EC.presence_of_element_located((By.CLASS_NAME,"captcha-prompt"))))
                    
                except:
                    getURL(driver,url)

                while len(getElementsByClass(driver,"captcha-prompt")) != 0:
                    getURL(driver,url)

                if len(getElementsByClass(driver,"content--error")) != 0:
                    handle404(driver,platform,fortmattedUN,userCheckHashmap)

                elif len(getElementsByClass(driver,"trn-tabs__item")) != 0:
                    tabs = getElementsByClass(driver,"trn-tabs__item")
                    # get overview
                    overviewText = ""
                    if waitOnElementByXpath(driver,5,xpaths["overview"]):
                        overviewText = getElementByXpath(driver,xpaths["overview"],1).text
                    
                    # get heroes
                    tabs[1].click()
                    # driver.get(url + "/heroes")
                    heroText = ""
                    heroText = getElementByCSS(driver,'div[data-v-7dcd1550][data-v-1bdd88b8]',5).text
                    
                    # get modes
                    tabs[2].click()
                    # driver.get(url + "/modes")
                    modeText = ""
                    modeText = getElementByCSS(driver,'div[data-v-49630b12][data-v-1bdd88b8]',5).text


                    if overviewText == "" or modeText == "" or heroText == "":
                        raise Exception(f"{fortmattedUN},{platform} : overview/mode/hero text null")
                    
                    overviewData = parseOverview(username=fortmattedUN,platform=platform,overviewTxt=overviewText)
                    overviewData['modes'] = parseModes(modeText)
                    overviewData['heros'] = parseHeros(heroText)

                    players[fortmattedUN] = {
                        "psn" : [],
                        "xbl" : [],
                        "uplay" : []
                        }

                    players[fortmattedUN][platform].append(overviewData)

                    deltaT = time.time() - playerStartTime
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
            mutex.acquire()
            users.append(user)
            file = open("ERRORLOG.json","r")
            errorlog = json.load(file)
            if user not in errorlog:
                errorlog[f"{username},{platform}"] = e
            file.close()
            file = open("ERRORLOG.json","w")
            json.dump(errorlog,file)
            file.close()
            mutex.release()




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
    time.sleep(5)

for item in threads:
    item.join()

