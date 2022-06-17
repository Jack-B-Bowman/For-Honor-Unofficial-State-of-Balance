import json


file = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\mergedUserDataFile3.json")
data = json.load(file)
newData = {}
for user in data:
    newData[user] = {
        "psn" : [],
        "xbl" : [],
        "uplay" : []
    }
    for stat in data[user]:
        if stat["platform"] == "psn":
            newData[user]["psn"].append(stat)
        if stat["platform"] == "xbl":
            newData[user]["xbl"].append(stat)
        if stat["platform"] == "uplay":
            newData[user]["uplay"].append(stat)

outputFile = open("newlyFormattedData.json","w")
outputFile.write(json.dumps(newData,indent=4))
