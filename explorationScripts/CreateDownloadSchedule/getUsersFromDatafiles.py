import json
import os
import time
# gets usernames and platforms of from directory of standard script output files

directory = "C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\datafiles"
# directory = "D:\\Archive\\UserScraper\\datafiles01-27-2023-14-22"
listOfNames = {}

print()
for filename in os.listdir(directory):

    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f) and f[-4:] == 'json':
        file = open(f,"r")
        print(f"\r{filename}",end="")
        try:
            newData = json.load(file)
            for player in newData:
                for platform in newData[player]:
                    if len(newData[player][platform]) > 0:
                        listOfNames[player + "," + platform] = time.time()


        except Exception as e:
            print(e)
            print(filename)
print()
print("dumping data...")
file = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\downloadSchedule\\DownloadedNames1231.json","w")
json.dump(listOfNames,file)
file.close()
