import fileManage2
from datetime import datetime
from pytz import timezone

# returns the elapsed milliseconds since the start of the program
def millis(time1, time2):
   dt = time1 - time2
   ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
   return ms

array = fileManage2.arrayOfDatabase()
for row in array:
    try:
        tz = row[3]
        #print(timezone)
        c = datetime.now(timezone(tz))
        currTime = datetime(c.year, c.month, c.day, c.hour, c.minute)
        dbtime = datetime.strptime(row[6], "%d/%m/%y %H:%M")
        if millis(currTime, dbtime) > 0:
            print("Attempting to send message to: {}".format(row[0]))
            fileManage2.changeBool(row[0], 'false')

            fileManage2.sendMessage(row)
            fileManage2.incrementDay(row[0])
            fileManage2.incrementDayPass(row[0])

            newTimeText = fileManage2.calculateNextDayText(tz)
            fileManage2.changeSendTime(row[0], newTimeText)
    except Exception as inst:
        print(type(inst))  # the exception instance
        print(inst)
