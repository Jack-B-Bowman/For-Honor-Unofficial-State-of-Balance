import json
import time
import random
import sys
import threading
from CommonSeleniumScraperFunctions import modeNames
from CommonSeleniumScraperFunctions import heroNames
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
mutex = threading.Lock()

arg = 0
if len(sys.argv) < 2:
    arg = 1
else: arg = int(sys.argv[1])

# read in the users csv
userFile = open("compiledUsers-04-06-1.csv","r")
usersFileLines = userFile.readlines()
userFile.close()
users = []
threads = []
threadData = {}


for line in usersFileLines:
    splitLine = line.split(",")
    platform = splitLine[0]
    username = splitLine[1][0:-1]
    splicedUsername = username.split("%20")
    splicedUsername = " ".join(splicedUsername)
    users.append((platform,username))

file = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\downloadSchedule\\downloadSchedule.json","r")
downloadSchedule = json.load(file)
file.close()

# shuffle the list for random selection from users
random.shuffle(users)


id = 0

"""
undefined 
H2
"""
nonExistantUsersFile = open(".\\failedUsers.csv","r")
nonExistantUsersList = nonExistantUsersFile.readlines()
failedUsersDict = {}
for user in nonExistantUsersList:
    failedUsersDict[user[0:-1]] = True

def progThread(id):
    totalUsers = len(users)
    while(len(users) > 0):

        display = ""

        progress = 100 - ((len(users) / totalUsers) * 100)

        for thread in threadData:
            display += f"{thread} : ΔT = {threadData[thread]['time']:.2f} \t"

        display += f"{progress:.2f}%"
        print(f"\r{display}",end="")
        time.sleep(5)

def checkIntegrety(username,platform,data):
    if data['platformInfo']['platformUserHandle'] != username:
        return False
    if data['platformInfo']['platformSlug'] != platform:
        return False
    return True

# username should not be in the url-coded (%20) form
def isDownloadUser(username,platform,download_schedule,failed_users):
    TIME_OFFSET = 86400 * 1
    user_hash_schedule = username + "," + platform
    user_hash_failed = platform + "," + username

    if user_hash_failed in failed_users:
        return False

    if user_hash_schedule not in download_schedule:
        return True

    if time.time() + TIME_OFFSET > download_schedule[user_hash_schedule]:
        return True
    
    return False


def getUser(driver,url):
            driver.get(url)
            time.sleep(1)

            # check for innitial state script

            # check for turnstile

            

            try:
                WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"#turnstile-wrapper > div")))
                time.sleep(5)
                driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
                driver.find_element(By.ID,"cf-stage").click()
                return 
            except Exception as e:
                time.sleep(100)
                return getUser(driver, url)

def parseSegments(stats,segments):
    for item in segments:
        # if the current item in segments is a hero and that hero exists. OutlandersH030PirateQueen is the pirate and SamuraiH029Faceless is kyoshin
        if item["type"] == "hero" and (item["metadata"]["name"] in heroNames or item["metadata"]["name"] == "OutlandersH030PirateQueen" or item["metadata"]["name"] == "SamuraiH029Faceless"):
            name = item["metadata"]["name"]
            if name == "OutlandersH030PirateQueen": name = "Pirate"
            if name == "SamuraiH029Faceless": name = "Kyoshin"
            name = heroNames[name]
            heroStats = item["stats"]
            stats["heros"][name]["wins"] = heroStats["wins"]["value"]
            stats["heros"][name]["losses"] = heroStats["losses"]["value"]
            stats["heros"][name]["kills"] = heroStats["killsP"]["value"]
            stats["heros"][name]["deaths"] = heroStats["deathsP"]["value"]
            stats["heros"][name]["assists"] = heroStats["assistsP"]["value"]
            stats["heros"][name]["time"] = heroStats["timePlayed"]["value"]
        
        # this section contains the user's global stats
        if item["type"] == "gameType":
            if item["metadata"]["name"] == "Player vs. Player Overview":
                globalStats = item["stats"]
                stats["reputation"] = globalStats["reputation"]["value"]
                stats["kills"] = globalStats["killsP"]["value"]
                stats["deaths"] = globalStats["deathsP"]["value"]
                stats["assists"] = globalStats["assistsP"]["value"]
                stats["wins"] = globalStats["wins"]["value"]
                stats["losses"] = globalStats["losses"]["value"]
                stats["time"] = globalStats["timePlayed"]["value"]
                stats["date"] = time.time()

        # this section contains the gamemode stats
        if item["metadata"]["name"] in modeNames:
                mode = item["metadata"]["name"]
                modeStats = item["stats"]
                stats["modes"][mode]["wins"]   = modeStats["wins"]["value"]
                stats["modes"][mode]["losses"] = modeStats["losses"]["value"]
                stats["modes"][mode]["kills"]  = modeStats["killsP"]["value"]
                stats["modes"][mode]["deaths"] = modeStats["deathsP"]["value"]
                stats["modes"][mode]["assists"]= modeStats["assistsP"]["value"]
                stats["modes"][mode]["time"]   = modeStats["timePlayed"]["value"]

        
    return stats

def handleErrors(username,platform,data,driver):
    error_message = data["errors"][0]["code"]
    if error_message == "CollectorResultStatus::NotFound":
        mutex.acquire()
        failedUsersFile = open("failedUsers.csv","a")
        failedUsersFile.write(platform + "," + username + "\n")
        failedUsersFile.close()
        mutex.release()
        return False

    if error_message == "CollectorResultStatus::ExternalError":
        # driver.quit()
        # time.sleep(5)
        # opts = uc.ChromeOptions()
        # opts.add_argument("--window-size=1020,900")  
        # opts.add_argument('--no-first-run --no-service-autorun --password-store=basic --no-default-browser-check --incognito')
        # driver = uc.Chrome(options=opts)
        time.sleep(60)
        return True
    
    mutex.acquire()
    file = open("errors.json","r")
    errors = json.load(file)
    file.close()
    mutex.release()

    if str(error_message) not in errors:
        errors[str(error_message)] = 1
    else: errors[str(error_message)] += 1

    mutex.acquire()
    file = open("errors.json","w")
    errors = json.dump(errors,file,indent=4)
    file.close()
    mutex.release()
    return False

def downloadThread(id):
    players = {}
    data = {}
    opts = uc.ChromeOptions()
    
    # opts.headless = True
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # opts.add_experimental_option("prefs", prefs)
    # opts.add_argument('--headless')
    # opts.add_argument('--proxy-server=103.147.118.17:9091')
    opts.add_argument("--window-size=1020,900")  
    opts.add_argument('--no-first-run --no-service-autorun --password-store=basic --no-default-browser-check --incognito')
    # opts.add_argument("--load-extension=C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\extensions\\extension_1_45_2_0")
    # opts.add_extension("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\extensions\\extension_1_45_2_0.crx")
    # opts.add_argument("--unsafe-pac-url")  
    # uc.TARGET_VERSION  = 104
    # driver = uc.Chrome(options=opts, use_subprocess=True, driver_executable_path = "C:\\\Program Files\\\Google\\\Chrome\\Application\\new_chrome.exe")
    driver = uc.Chrome(options=opts)
    # driver.implicitly_wait(10)
    # driver = uc.Chrome(options=opts)
    # driver.get("https://chrome.google.com/webstore/detail/ublock-origin/cjpalhdlnbpafiamejdnhcphjbkeiagm?hl=en")
    # installBtn = getElements(driver,"g-c-Hf",waitTime=5)
    # installBtn[0].click()
    time.sleep(1)
    # driver.get("chrome-extension://cjpalhdlnbpafiamejdnhcphjbkeiagm/dashboard.html#1p-filters.html")
    # time.sleep(5)
    # add ublock settings
    # driver.execute_script("document.evaluate('/html/body/div[2]/div/div[2]/div[6]/div[1]/div/div/div/div[5]/div[1]/pre/span/span', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.innerHTML=arguments[0];",ublockSettings)
    # enable button
    # driver.execute_script("document.evaluate('/html/body/div[1]/p[2]/button[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.disabled=false;")
    # Alert(driver).accept()
    # time.sleep(10)
    # time.sleep(60)
    num = 1
    while len(users) > 0:
        mutex.acquire()
        user = users.pop(0)
        mutex.release()

        platform = user[0]
        username = user[1]

        url_name = username

        splitUsername = username.split("%20")
        username = " ".join(splitUsername)

        if isDownloadUser(username,platform,downloadSchedule,failedUsersDict):

            url = f'https://tracker.gg/for-honor/profile/{platform}/{url_name}/pvp'
            # url = "https://api.tracker.gg/api/v2/for-honor/standard/profile/xbl/Poor%20yves?1"
            data = getUser(driver,url)

            if "errors" in data:
                retry = handleErrors(username,platform,data,driver)
                if retry and len(users) > 100:
                    mutex.acquire()
                    users.append((platform,url_name))
                    mutex.release()

            if "data" in data:
                # each stats has the date (in seconds since epoch) along with the player's rep time played and PVP stats
                # these include total kills, deaths, assists, wins, and losses. As well as kills, deaths, assists, wins, and losses by mode
                # they also include kills, deaths, assists, wins, losses, and time played for each hero. I use time played as a substitute for rep.
                # these stats do not include K/D/A/W/L for each hero per mode. I cannot say for sure that player "A" has a 63% winrate in dominion as Berserker.
                # this kind of stat could be approximated by using players that play almost exclusivly that mode though
                mutex.acquire()
                file = open("stat_format.json","r")
                stats = json.load(file)
                file.close()
                mutex.release()
                
                players[username] = {
                "psn" : [],
                "xbl" : [],
                "uplay" : []
                }
                stats = parseSegments(stats,data["data"]["segments"])
                stats["platform"] = platform
                stats["faction"] = data["data"]["metadata"]["factionKey"]
                players[username][platform].append(stats)

                num += 1
                if(num % 50 == 0):
                    dataFile = open(f".\\datafiles\\data{str(id)}-{str(num)}.json","a")
                    json.dump(players,dataFile)
                    dataFile.close() 
                    players = {}
                    # time.sleep(20)


    dataFile = open(f".\\datafiles\\dataFinal-{id}.json","a")
    dataFile.write(json.dumps(players))
    dataFile.close()
    players = {}
    return

number = len(users)

gui = threading.Thread(target=progThread, args=[99])
gui.start()
threads.append(gui)

for n in range(arg):
    t = threading.Thread(target=downloadThread, args=[n])
    t.start()
    threads.append(t)
    time.sleep(20)

for item in threads:
    item.join()





