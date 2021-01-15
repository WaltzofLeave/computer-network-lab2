import threading

class runScriptThread(threading.Thread):
    def __init__(self, funcName, *args):
        threading.Thread.__init__(self)
        self.args = args
        self.funcName = funcName

    def run(self):
        try:
            self.funcName(*self.args)
        except Exception as e:
            raise e