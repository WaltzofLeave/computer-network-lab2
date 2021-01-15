from runscriptthread import runScriptThread
import threading
import time

class eventScriptThread(threading.Thread):
    def __init__(self, funcName, *args):
        threading.Thread.__init__(self)
        self.args = args
        self.funcName = funcName
        self.result = None

    def run(self):
        try:
            self.result = self.funcName(*self.args)
        except Exception as e:
            raise e

    def getreturnedvalue(self):
        return self.result


class Event():
    name = ""
    func = None
    args = None

    def __init__(self,name:str,func,*args):
        self.name = name
        self.func = func
        self.args = args


    def deal(self):
        dealthread = eventScriptThread(self.func,*self.args)
        dealthread.start()
        dealthread.join()
        returned = dealthread.getreturnedvalue()
        print("Event"+self.name+"dealt successfully")
        return returned

def plus1(x,y):
    print(x + y + 1)
    return x + y + 1


class EventQueue():
    queue = None

    def __init__(self):
        self.queue = []
        self.start()

    def add(self,event:Event):
        lock = threading.Lock()
        lock.acquire()
        self.queue.append(event)
        lock.release()

    def deal(self):
        lock = threading.Lock()
        lock.acquire()
        event = self.queue[0]
        self.queue.remove(event)
        lock.release()
        return event.deal()
    def __startfunction(self):
         while True:
             lock = threading.Lock()
             lock.acquire()
             lenth = len(self.queue)
             if not lenth == 0:
                 self.deal()
             lock.release()
             time.sleep(0.01)
    def start(self):
        e = eventScriptThread(self.__startfunction)
        e.start()

# queue = EventQueue()
# queue.start()
# queue.add(Event('plus1',plus1,1,2))
# queue.add(Event('plus1',plus1,3,4))
# time.sleep(10)
# queue.add(Event('plus1',plus1,5,6))