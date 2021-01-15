import time
from runscriptthread import runScriptThread
from Event import EventQueue
from Event import Event
class Timer:
    timechecker = None
    timethread = None
    valid = None
    eventqueue = None
    timeroutfun = None
    timeroutargs = None
    def __init__(self,eventqueue:EventQueue,timeroutfun,*timeroutargs):
        self.timechecker = []
        self.valid = True
        self.eventqueue = eventqueue
        self.timeroutfun = timeroutfun
        self.timeroutargs = timeroutargs
    def timerfunc(self, count_time: int, timercheckerl: list) -> None:
        print("Timer start")
        time.sleep(count_time)
        timercheckerl.append('TimeOut')
        if self.valid:
            self.eventqueue.add(Event('TimeOut',self.timeroutfun,*self.timeroutargs))




    def starttimer(self, count_time: int):
        timethread = runScriptThread(self.timerfunc, count_time, self.timechecker)
        timethread.start()
        self.timethread = timethread

    def stoptimer(self):
        self.valid = False
    def isTimeOut(self):
        if not len(self.timechecker) == 0:
            print("Time out detected!")
            return True
        else:
            return False


queue = EventQueue()
l = []
def timeroutfun(a,b,l):
    print("Timerout",a,b,l)
    l.append("TimeOut")

# mytimer = Timer(queue, timeroutfun, 1, 2, l)
# mytimer.starttimer(5)
# for i in range(1,7):
#     time.sleep(1)
#     print(l)
# mytimer.stoptimer()
# while True:
#     time.sleep(1)
#     print(l)