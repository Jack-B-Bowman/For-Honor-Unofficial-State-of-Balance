
file = open("compiledUsers-08-06-1.csv","r")
text = file.readlines()
file.close()
users = {}

for line in text:
    if line in users:
        users[line] += 1
    else:
        users[line] = 0

file = open("compiledUsers-08-06-1.csv", "w")
for line in users:
    file.write(line)

file.close()
