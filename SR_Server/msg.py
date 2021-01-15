import random

import re
class Msg:
    data = None
    checksum = None
    seqnum = None
    @classmethod
    def encode(cls,msg_cls):
        msg = msg_cls
        if msg.checksum is not None:
            cks = str(msg.checksum)
        else:
            cks = 'None'
        if msg.seqnum is not None:
            seq = str(msg.seqnum)
        else:
            seq = 'None'
        string = msg.data + '||' + cks + '||' + seq
        return string.encode('utf-8')
    @classmethod
    def decode(cls,msg_bin):
        msg = msg_bin
        string = bytes.decode(msg_bin)
        items = string.split('||')
        items = list(items)
        if items[1] == 'None':
            items[1] = None
        if items[2] == 'None':
            items[2] = None
        if items[1] is not None:
            items[1] = int(items[1])
            if items[1] == 0:
                items[1] = False
            else:
                items[1] = True
        msg = Msg(*items)
        return msg

    def __init__(self, data, checksum=None, seqnum=None):
        """

        :param data:
        :param checksum: True or False
        :param seqnum:
        """
        self.make_pkt(data, checksum, seqnum)

    def make_pkt(self, data, checksum=None, seqnum=None):
        self.data = data
        if checksum is True:
            self.checksum = 1
            self.checksum = self.calculate_checksum()
        else:
            self.checksum = None
        self.seqnum = seqnum

    def calculate_checksum(self):
        """
        Modify This Function To change Implementation for CheckSum,If the implementation change,the function corrupt should also be changed
        :return: should always return self.checksum
        """
        if self.checksum is None:
            self.checksum = 0
        else:
            self.checksum = 1
        return self.checksum

    def corrupt(self, rate=0.95):
        if self.checksum == 1:
            randnum = random.randint(0, 100)
            if randnum > rate * 100:
                return True
            else:
                return False

    def notcorrupt(self,rate=0.95):
        return not self.corrupt(rate)

    def isack(self, seq):
        if self.data == 'ack'+str(seq) or self.data == 'ACK'+str(seq) or self.data == "Ack"+str(seq):
            return True
        else:
            return False






