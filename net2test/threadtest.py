import threading
import time
import multiprocessing

class runScriptThread(threading.Thread):
    def __init__(self, funcName, *args):
        threading.Thread.__init__(self)
        self.args = args
        self.funcName = funcName

    def run(self):
        try:
            self.funcName(*(self.args))
        except Exception as e:
            raise e


def timer(timercheck):
    time.sleep(10)
    timercheck.append(True)

def mission(missioncheck):
    time.sleep(9)
    missioncheck.append(True)

timercheck = []
missioncheck = []
newThread1 = runScriptThread(timer, (timercheck))
newThread2 = runScriptThread(mission, (missioncheck))
newThread1.start()
newThread2.start()
while True:
    if len(timercheck) == 1:
        print("Time out")
        break
    if len(missioncheck) == 1:
        print("Mission accomplished")
        break;
    time.sleep(1)





