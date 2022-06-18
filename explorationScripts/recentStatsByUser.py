import matplotlib.pyplot as plt
import numpy as np
import sqlite3
conn = sqlite3.connect("FH.db")
crsr = conn.cursor()
seasonStartDate = 1655395200
user = "vincent_van_goy"
crsr.execute(f"SELECT * from stat where username = '{user}' and stat.UTCSeconds > {seasonStartDate}")
ans = crsr.fetchall()
ans.sort(key=lambda y:y[4])
last = ans[0]
first = ans[-1]

winrate = ((first[9] - last[9]) / ((first[9] - last[9]) + (first[10] - last[10]))) * 100
KDRatio = ((first[6] - last[6]) / (first[7] - last[7]))
print(f"your winrate over the last {(first[9] - last[9]) + (first[10] - last[10])} games is {winrate:.2f}%\nyour KD ratio is {KDRatio:.2f}")