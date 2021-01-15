import socket
import random
import msg
from msg import Msg
import threading
import _thread
import time
from timer import timer
from runscriptthread import runScriptThread




class MyServer:
    """
    A Server socket automatically deal with needs
    """
    ip = None
    port = None
    old_socket = None

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
            self.func(new_socket)

    def func(self, new_socket):
        """
        new_socket is a socket connect to the socket that sending messages to this server.
        change this function to implement the behaviour the server do
        :param new_socket:
        :return:
        """
        buffer = []
        self.rdt_send_3(new_socket)

    def rdt_send_3(self, new_socket):
        queue = []
        seq = 0
        inputthread = runScriptThread(self.userinput, queue)
        inputthread.start()
        while True:
            while True:
                lock = threading.Lock()
                time.sleep(1)
                lock.acquire()
                if len(queue) != 0:
                    lock.release()
                    break
                lock.release()
            lock = threading.Lock()
            lock.acquire()
            data = queue[0]
            queue.remove(queue[0])
            lock.release()
            sndpkt = self.make_pkt(data, True, seq)
            self.udt_send(new_socket, sndpkt)
            atimer = timer()
            atimer.starttimer(3)
            rcvpkt = []
            rcvthread = runScriptThread(self.rdt_rcv, (new_socket, rcvpkt))
            rcvthread.start()
            while True:
                if not len(rcvpkt) == 0:
                    rcvpkt = rcvpkt[0]
                    if self.corrupt(rcvpkt) or self.isack(rcvpkt,seq):
                        rcvpkt = []
                        rcvthread = runScriptThread(self.rdt_rcv, (new_socket, rcvpkt))
                        rcvthread.start()
                        continue
                    else:
                        break
                if atimer.isTimeOut():
                    self.udt_send(new_socket, sndpkt)
                    atimer = timer()
                    atimer.starttimer(3)
                    continue
            if seq == 0:
                seq = 1
            else:
                seq = 0

    def userinput(self, queue):
        msg = input("Please input message:")
        print("Adding message to the event queue.........")
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


