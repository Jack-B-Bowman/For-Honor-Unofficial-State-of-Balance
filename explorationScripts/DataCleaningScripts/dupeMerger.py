import json
import os

directory = "C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\datafiles\\New folder (2)"
first = True
originalFile = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\updatedUserStats05-18-1.json","r")
mergedData = json.load(originalFile)
numberOfDupes = 0
numberOfActive = 0
count = 0
for filename in os.listdir(directory):

    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        file = open(f,"r")
        newData = json.load(file)
        for user in newData:
            count += 1

            if(count % 1000 == 0):
                print(count)

            if user in mergedData:
                numberOfDupes += 1
                for platform in newData[user]:
                    platformStatsList = newData[user][platform]
                    for stat in platformStatsList:
                        isNew = True
                        originalStats = mergedData[user][platform]
                        for compareStat in originalStats:
                            if compareStat["time"] == stat["time"]:
                                isNew = False
                        if isNew:
                            numberOfActive += 1
                            originalStats.append(stat)
                            originalStats = sorted(originalStats,key=lambda d: d['time'])
                            mergedData[user][platform] = originalStats

            else:
                count +=1 
                mergedData[user] = newData[user]
        file.close()




mergedFile = open("updatedUserStats05-18-2.json","w")
mergedFile.write(json.dumps(mergedData))
mergedFile.close()