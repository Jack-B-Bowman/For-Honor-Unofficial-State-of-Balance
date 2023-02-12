import json
import csv
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
conn = sqlite3.connect("FH.db")
crsr = conn.cursor()

# seasonStartDate = 1655395200 # true season start
seasonStartDate = 1656547619 # post conq nerf 
# seasonStartDate = 1658970014
seasonStartDate = 1658966400 # Medjay
seasonStartDate = 1663248434 # dodge
seasonStartDate = 1666137644 # crossplay phase 2
seasonStartDate = 1666656044 # kensei hitstun+matchmaking

brokenPlayers = []

sql = f"""

SELECT reputation from (
select username,platform, reputation, max(UTCSeconds), count(username) as num
from stat 
WHERE UTCSeconds > {seasonStartDate}
group by username,platform
) where num > 2;
"""
crsr.execute(sql)
ans = crsr.fetchall()
print(np.mean(ans))
print(np.median(ans))


