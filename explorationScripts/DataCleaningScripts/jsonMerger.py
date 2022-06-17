import json
import pandas as pd
import os

mergedList = []

directory = "C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\datafiles"
first = True
for filename in os.listdir(directory):

    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        file = open(f,"r")
        if first:
            first = False
            mergedList = json.load(file)
        else:
            data = json.load(file)
            mergedList = mergedList + data
        file.close()

mergedFile = open("mergedFile04-23-1.json","w")
mergedFile.write(json.dumps(mergedList,indent=4))
mergedFile.close()