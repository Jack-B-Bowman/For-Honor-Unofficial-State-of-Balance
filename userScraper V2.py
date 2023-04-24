import json
import time
import sys
import threading
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

mutex = threading.Lock()

arg = 0
if len(sys.argv) < 2:
    arg = 1
else: arg = int(sys.argv[1])

players = []

def URLiseName(name):
    splitUsername = name.split(" ")
    FormattedUsername = "%20".join(splitUsername)
    return FormattedUsername

def getData(data):
    playerData = []
    for item in data:
        player = item
        username = URLiseName(player["owner"]["metadata"]["platformUserHandle"])
        platform = player["owner"]["metadata"]["platformSlug"]
        playerData.append((platform,username))
    return(playerData)

def downloadThread(id):
    opts = uc.ChromeOptions()
    # opts.headless = True
    opts.add_argument('--headless')
    # opts.add_argument('--proxy-server=103.147.118.17:9091')
    opts.add_argument("--window-size=1020,900")  
    # opts.add_argument("--unsafe-pac-url")  

    driver = uc.Chrome(options=opts)

    timeToStop = False
    # skip = 380500
    skip = 0
    cutoffCounter = 0
    while not timeToStop:
        cutoffCounter += 1
        # url = f"https://api.tracker.gg/api/v1/for-honor/standard/leaderboards?type=stats&platform=all&board=KdRatioP&gameType=pvp&skip={skip}&take=100"
        url = f"https://api.tracker.gg/api/v1/for-honor/standard/leaderboards?type=stats&platform=all&board=Wins&gameType=pvp&skip={skip}&take=100"
        driver.get(url)
        time.sleep(1)
        try:
            WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.TAG_NAME,"pre"))
            )
            data = json.loads(driver.find_element(by=By.TAG_NAME,value="pre").text)["data"]["items"]
        except Exception as e:
            print(e)
            time.sleep(10)
            driver.get(url)
            time.sleep(1)
            WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.TAG_NAME,"pre"))
            )
            data = json.loads(driver.find_element(by=By.TAG_NAME,value="pre").text)["data"]["items"]

        # print(1)

        playerList = getData(data)
        if len(playerList) > 0:
            players.extend(playerList)
        else:
            timeToStop = True
        if cutoffCounter > 4000:
            timeToStop = True

        # print(2)        

        skip += 100
        print(f"users scraped = {skip}")
        file = open("usersTesting04-06-1.txt","a")
        for user in playerList:
            try:
                file.write(user[0] + "," + user[1] + "\n")
            except:
                print("weird break")
        file.close()

    


threads = []
for n in range(arg):
    t = threading.Thread(target=downloadThread, args=[n])
    t.start()
    threads.append(t)
    time.sleep(180)

for item in threads:
    item.join()





