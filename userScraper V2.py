import json
import time
import sys
import threading
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
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
    # opts.add_argument('--headless')
    # opts.add_argument('--proxy-server=103.147.118.17:9091')
    opts.add_argument("--window-size=1020,900")  
    # opts.add_argument("--unsafe-pac-url")  

    driver = uc.Chrome(options=opts, use_subprocess=True, driver_executable_path = "C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\chromedriver.exe")

    timeToStop = False
    skip = 380500
    cutoffCounter = 0
    while not timeToStop:
        cutoffCounter += 1
        # url = f"https://api.tracker.gg/api/v1/for-honor/standard/leaderboards?type=stats&platform=all&board=KdRatioP&gameType=pvp&skip={skip}&take=100"
        url = f"https://api.tracker.gg/api/v1/for-honor/standard/leaderboards?type=stats&platform=all&board=Wins&gameType=pvp&skip={skip}&take=100"
        driver.get(url)
        time.sleep(1)
        try:
            data = json.loads(driver.find_element(by=By.TAG_NAME,value="pre").text)["data"]["items"]
        except:
            time.sleep(4)
            driver.get(url)
            time.sleep(1)
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
        file = open("usersTesting12-03-1.txt","a")
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





