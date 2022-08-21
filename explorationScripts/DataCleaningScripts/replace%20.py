import sqlite3
conn = sqlite3.connect("FH.db")
crsr = conn.cursor()
crsr.execute("""SELECT username,platform,playerID from stat where username like '%20%' and platform='xbl'""")
ans = crsr.fetchall()
crsr.execute('BEGIN TRANSACTION')
for item in ans:
    splitUsername = item[0].split("%20")
    fortmattedUN = " ".join(splitUsername)
    sql = f"""update stat set username = '{fortmattedUN}' where playerID = {item[2]}"""
    crsr.execute(sql)

conn.commit()
conn.close()