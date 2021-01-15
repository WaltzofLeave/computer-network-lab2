import socket
import random
import msg
from msg import Msg
import threading
import _thread
import time
from timer import Timer
from runscriptthread import runScriptThread
from myserver import MyServer




class MyClient:
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
        print("111")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ip_port = (host, port)
        s.connect(ip_port)
        return s

    def mainloop(self):
        print("Into main loop::")
        while True:
            new_socket = self.old_socket
            self.func(new_socket)

    def func(self, new_socket):
        """
        new_socket is a socket connect to the socket that sending messages to this server.
        change this function to implement the behaviour the server do
        :param new_socket:
        :return:
        """
        print("Finish initalizing. into code ")
        self.GBN_rcv(new_socket)

    def GBN_rcv(self, new_socket):
        seq = 0
        rcvpkt = []
        while True:
            self.rdt_rcv(new_socket,rcvpkt)
            pkt = rcvpkt[0]
            print(pkt.data)
            if not self.corrupt(pkt) and int(pkt.seqnum) == int(seq):
                self.deliver_data(pkt.data,'data.txt')
                self.udt_send(new_socket, Msg('ACK' + str(seq),True,seq), 1)
                seq = seq + 1
            rcvpkt = []



    def udt_send(self,newsocket:socket.socket,msg:Msg,rate = 0.95):
        # randnum = random.randint(0,100)
        # if randnum < rate * 100:
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



isserver = False
if isserver:
    server = MyServer('127.0.0.1',10006)
    serverthread = runScriptThread(server.mainloop)
    serverthread.start()
    #serverthread.join()
else:
    client = MyClient('127.0.0.1',10005)
    clientthread = runScriptThread(client.mainloop)
    clientthread.start()
    #clientthread.join()