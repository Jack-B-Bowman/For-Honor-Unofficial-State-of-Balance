import matplotlib.pyplot as plt
import seaborn as sns

file = open("anomolies.txt","r")
data = file.readlines()
file.close()

numbers = []
for line in data:
    line = line[:-1]
    datum = line.split(',')
    numbers.append(datum[3])


ax = sns.distplot(numbers,hist=True)
plt.show()
# 1656228329