


filesToMerge = [
    "users.csv",
    "users2.csv",
    "users3.csv"
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

combinedFile = open("compiledUsers.csv","a")
combinedFile.writelines(users)
combinedFile.close()