import socket
import random
import msg
from msg import Msg
import threading
import _thread
import time
from timer import Timer
from runscriptthread import runScriptThread

from Event import EventQueue
from Event import Event




class MyServer:
    """
    A Server socket automatically deal with needs
    """
    ip = None
    port = None
    old_socket = None
    new_socket = None
    def __init__(self, ip, port):
        """

        :param ip: The server's ip
        :param port:  The server's port
        """
        self.ip = ip
        self.port = port
        self.old_socket = self.create_server_socket(ip,port)

    def create_server_socket(self,host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ip_port = (host, port)
        s.bind(ip_port)
        s.listen(50)
        return s

    def mainloop(self):
        while True:
            new_socket, address = self.old_socket.accept()
            self.new_socket = new_socket
            self.func(new_socket)

    def func(self, new_socket):
        """
        new_socket is a socket connect to the socket that sending messages to this server.
        change this function to implement the behaviour the server do
        :param new_socket:
        :return:
        """

        self.GBN_send(new_socket)



    def recv_thread_fun(self, window):
        while True:
            rcvpkt = []
            self.rdt_rcv(self.new_socket,rcvpkt)
            window.recv(rcvpkt[0])

    def GBN_send(self,newsocket, window_size=10):
        queue = EventQueue()
        window = Window(self,queue,10)
        rcvthread = runScriptThread(self.recv_thread_fun,window)
        with open('a.txt','r') as f:
            filestring = f.read()
            messages = filestring.split('\n')
        while True:
            for msg in messages:
                success = False
                while not success:
                    success = window.send(msg)
                    time.sleep(1)








    def userinput(self, queue):
        while True:
            msg = input("Please input message:")
            print("Adding message to the event queue.........")
            if msg[0:4] == 'File':
                try:
                    with open(msg[5:]) as f:
                        msg = f.read()
                except Exception as e:
                    print("Fail to read file.Check filename.")
                    continue
            lock = threading.Lock()
            lock.acquire()
            queue.append(msg)
            lock.release()
            print("Finish adding message to event queue,please wait for processing.")

    def udt_send(self,newsocket:socket.socket,msg:Msg,rate = 0.95):
        randnum = random.randint(0,100)
        if randnum < rate * 100:
            newsocket.send(Msg.encode(msg))

    def rdt_rcv(self, newsocket: socket.socket, rcvpkt:list):
        msg = newsocket.recv(65510)
        ## not allow me to use Msg here
        newmsg = Msg.decode(msg)
        rcvpkt.append(newmsg)

    def corrupt(self,msg: Msg) -> bool:
        return msg.corrupt()

    def notcorrupt(self,msg: Msg) -> bool:
        return msg.notcorrupt()

    def extract(self,msg:Msg) -> str:
        return msg.data

    def isack(self,msg:Msg,seq:int):
        return msg.isack(seq)

    def make_pkt(self, data, checksum=None, seq=None):
        m = Msg(data, checksum, seq)
        return m

    def deliver_data(self,data:str,filename:str):
        try:
            with open(filename, 'a+') as f:
                f.write(data)
        except Exception as e:
            print('fail to deliver data')


class Window:
    base = 0
    nextseqnum = 0
    N = 0
    sndpkt = None
    queue = None

    server: MyServer = None
    timer = None

    def __init__(self, server, queue, window_size=10):
        self.queue = queue
        self.N = window_size
        self.sndpkt = []
        self.server = server

    def starttimer(self):
        if self.timer is not None:
            self.timer.stoptimer()
        self.timer = Timer(self.queue, self.timeoutfun, self)
        self.timer.starttimer(10)

    def send(self, msg: str) -> bool:
        if not self.base < self.nextseqnum + self.N:
            return False
        pkt = self.server.make_pkt(msg, True, self.nextseqnum)
        self.sndpkt.append(pkt)
        self.server.udt_send(self.server.new_socket,pkt)
        if self.base == self.nextseqnum:
            self.starttimer()
        return True
    def recv(self,msg):
        if self.server.notcorrupt(msg):
            self.base = msg[0].seqnum + 1
            if self.base == self.nextseqnum:
                self.timer.stoptimer()
            else:
                self.starttimer()
    def timeoutfun(self, window):
        base = window.base
        nextseqnum = window.nextseqnum
        window.starttimer()
        for i in range(base, nextseqnum):
            window.server.udt_send(window.server.new_socket, window.sndpkt[i])
