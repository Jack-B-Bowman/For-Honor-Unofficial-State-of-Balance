


filesToMerge = [
    "compiledUsers-12-04-1.csv",
    "usersTesting03-15-1.txt",
    "usersTesting04-06-1.txt"
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

combinedFile = open("compiledUsers-04-06-1.csv","a")
combinedFile.writelines(users)
combinedFile.close()