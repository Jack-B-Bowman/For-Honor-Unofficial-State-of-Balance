userFile = open("C:\\Users\\Jack Bowman\\Documents\\Programs\\PytScripts\\UserScraper\\usersTesting06-18-1.txt","r")
users = userFile.readlines()
userFile.close()
userFile = open("UserFiles\\users4.csv","w")
for user in users:
    splitLine = user.split('/')
    userFile.write(splitLine[3] + "," + splitLine[4] + "\n")
userFile.close()