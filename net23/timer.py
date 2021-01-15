import time
from runscriptthread import runScriptThread
class timer:
    timechecker = None
    timethread = None

    def __init__(self):
        self.timechecker = []

    def timerfunc(self, count_time: int, timercheckerl: list) -> None:
        print("Timer start")
        time.sleep(count_time)
        timercheckerl.append('TimeOut')
        print(self.timechecker)

    def starttimer(self, count_time: int):
        timethread = runScriptThread(self.timerfunc, count_time, self.timechecker)
        timethread.start()

    def isTimeOut(self):
        if not len(self.timechecker) == 0:
            print("Time out detected!")
            return True
        else:
            return False
