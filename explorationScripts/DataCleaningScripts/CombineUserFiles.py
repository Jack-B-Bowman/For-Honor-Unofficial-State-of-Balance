


filesToMerge = [
    "UserFiles\\users.csv",
    "UserFiles\\users2.csv",
    "UserFiles\\users3.csv",
    "UserFiles\\users4.csv",
    "UserFiles\\users5.csv",
    "UserFiles\\users6.csv",
    "compiledUsers-06-27-1.csv"
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

combinedFile = open("compiledUsers-08-06-1.csv","a")
combinedFile.writelines(users)
combinedFile.close()