


filesToMerge = [
    "UserFiles\\users.csv",
    "UserFiles\\users2.csv",
    "UserFiles\\users3.csv",
    "UserFiles\\users4.csv",
    "compiledUsers.csv"
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

combinedFile = open("compiledUsers-06-18-1.csv","a")
combinedFile.writelines(users)
combinedFile.close()