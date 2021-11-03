import sqlite3
import fileManage2

conn = sqlite3.connect('test2.db')
value = conn.execute(
    "SELECT DAY_VAL FROM DAY;")
for row in value:
    day = row[0]
day = day + 1
conn.execute("UPDATE DAY set DAY_VAL = {};".format(day))
conn.commit()
print("Set day to {}".format(day))

fileManage2.updateAllToTrue()
print("Updated CAN_SEND to true, new day has started")

fileManage2.activateWatch()
print("Activating watch for STOP emails")

changes = fileManage2.clearPhoneCache()
print("Cleared Phone Cache of {} values".format(changes))
