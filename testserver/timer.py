import time
from runscriptthread import runScriptThread
class timer:
    timechecker = None
    timethread = None

    def __init__(self):
        timechecker = []

    def timerfunc(self, count_time: int, timerchecker: list) -> None:
        time.sleep(count_time)
        timerchecker.append('TimeOut')

    def starttimer(self, count_time: int):
        timethread = runScriptThread(self.timerfunc, (self, count_time, self.timechecker))
        timethread.start()

    def isTimeOut(self):
        if not len(self.timechecker) == 0:
            return True
        else:
            return False
