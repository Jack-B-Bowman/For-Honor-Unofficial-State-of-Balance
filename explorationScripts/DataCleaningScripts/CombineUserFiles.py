


filesToMerge = [
    "compiledUsers-10-23-1.csv",
    ".\\UserFiles\\usersTesting12-03-1.txt"
]

users = {}

for file in filesToMerge:
    fileToMerge = open(file,"r")
    lines = fileToMerge.readlines()
    fileToMerge.close()
    for line in lines:
        if line in users:
            users[line] += 1
        else:
            users[line] = 0

combinedFile = open("compiledUsers-12-04-1.csv","a")
combinedFile.writelines(users)
combinedFile.close()