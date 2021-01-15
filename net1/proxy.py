import socket
import re
import traceback

class message:

    httpmsg = None

    def __init__(self, httpmsg):
        self.httpmsg = httpmsg

    def __eq__(self, other):
        if not isinstance(other,message):
            return False
        if self.httpmsg is None and other.httpmsg is None:
            return True
        if self.httpmsg is not None and other.httpmsg is None:
            return False
        if self.httpmsg is None and other.httpmsg is not None:
            return False
        if self.httpmsg['commandline'] == other.httpmsg['commandline']:
            return True
    @classmethod
    def createmessage(cls, msg,mtype='response'):
        if isinstance(msg,bytes) or isinstance(msg,str):
            return message(cls.__inside_parseHTTP(msg,mtype))
        else:
            return message(msg)
    @staticmethod
    def __inside_parseHTTP(msg,mtype):
        """
        :param msg: a binary message
        :return: a dictionary
        """
        if mtype == 'request':
            ans = {}
            ans['msg_binary'] = msg
            print(msg)
            msg = msg.decode('utf-8')
            ans['msg-utf-8'] = msg
            msgs = msg.split('\r\n')
            commandline = msgs[0]
            commandline = commandline.split(' ')
            ans['command'] = commandline[0]
            ans['url'] = commandline[1]
            ans['version'] = commandline[2]
            ans['commandline'] = commandline
        elif mtype == 'response':
            ans = {}
            ans['msg_binary'] = msg
            print(msg)
        return ans

class cache:
    cached = None
    length = 10

    def checklength(self):
        while len(self.cached) >= self.length:
            self.cached.remove(self.cached[0])

    def __init__(self):
        self.cached = []

    def __iter__(self):
        return [x[0] for x in self.cached].__iter__()

    def add1(self, item):
        item0 = None
        item1 = None
        if not isinstance(item,tuple):
            print("Cache method add use tuple !")
            return
        if len(item) != 2:
            print("Cache method add should add a tuple of size 2")
            return
        if isinstance(item[0],message):
            item0 = item[0]
        else:
            item0 = message.createmessage(item[0],'request')
        if isinstance(item[1],message):
            item1 = item[1]
        else:
            item1 = message.createmessage(item[1],'response')

        self.cached.append((item0, item1))
        self.checklength()

    def add(self, item1, item2):
        self.add1(tuple((item1, item2)))
    def getcachedresponse(self,_item):
        item = None
        if isinstance(_item,message):
            item = _item
        else:
            item = message.createmessage(_item,'request')

        if item in self:
            for pair in self.cached:
                #if pair[0] == item:
                print("Using cached response!")
                return pair[1].httpmsg['msg_binary']
                #else:
                #    print("CACHE INSIDE ERROR!")
                #    exit(0)


def addfunction(url,usr= None,fish = False):
    urllist = []
    if url in urllist:
        print("被禁用了")
        return False,url
    usrlist = []
    if usr is not None and usr in usrlist:
        return False,url
    fish = {'http://today.hit.edu.cn/':'http://jwts.hit.edu.cn'}
    if fish:
        if url in fish:
            return True,fish[url]
        else:
            return True,url
    else:
        return True,url
def createmessage(msg,mtype):
    return message.createmessage(msg,mtype)


def parseHTTP(msg,mtype):
    if mtype == 'request':
        ans = {}
        ans['msg_binary'] = msg
        print(msg)
        msg = msg.decode('utf-8')
        ans['msg-utf-8'] = msg
        msgs = msg.split('\r\n')
        commandline = msgs[0]
        commandline = commandline.split(' ')
        ans['command'] = commandline[0]
        ans['url'] = commandline[1]
        ans['version'] = commandline[2]
        ans['commandline'] = commandline
    elif mtype == 'response':
        ans = {}
        ans['msg_binary'] = msg
        print(msg)
    return ans


def get_host_port(host_port_str):
    host_string, port_string = host_port_str.split(':')
    host = host_string
    port = int(port_string)
    return host,port

def create_server_socket(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ip_port = (host, port)
    s.bind(ip_port)
    s.listen(50)
    return s

def create_client_socket(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("CP1")
    ip_port = (host, port)
    print("CP2")
    s.connect(ip_port)
    print("CP3")
    return s

def changeurl(msg,url):
    msg = msg.decode('utf-8')
    #print(msg)
    msg = msg.split(' ')
    ans = ''
    msg[1] = url
    for string in msg:
        ans = ans + string + ' '
    ans = ans[:-1]
    msg = ans
    msg = str.encode(msg)
    msg = msg.decode('utf-8')
    msg = msg.split('\r\n')

    dealurl = url
    head_pat = re.compile(r'.*://')
    if head_pat.match(dealurl):
        dealurl = re.split(r'://', dealurl)[-1]
    dealurl = dealurl.split(r'/')[0]

    msg[1] ='Host: '+ dealurl
    ans = ''
    for string in msg:
        ans = ans +string + '\r\n'
    msg = ans
    #print(msg)
    msg = str.encode(msg,"utf-8")
    return msg

#def returnestablish():
#    return b'HTTP/1.1 200 Connection Established \r\n\r\n'
proxy = create_server_socket('0.0.0.0', 10005)

new_proxy_connection, address = proxy.accept()
server = None
counter = 0

mycache = cache()

while True:
    counter = counter + 1
    print('iteration ' + str(counter))
    new_proxy_connection, address = proxy.accept()
    try:
        msg = new_proxy_connection.recv(65510)
        print("请求报文：")
        print(msg.decode('utf-8'))
        if createmessage(msg,'request') in mycache:
            recmsg = mycache.getcachedresponse(msg)
            #recmsg = bytes.encode(recmsg,'utf-8')
            new_proxy_connection.send(recmsg)
            mycache.add(msg, recmsg)
            print("接收到的报文:")
            print(recmsg)
            continue
        httpmsg = parseHTTP(msg,'request')
        permit,url = addfunction(httpmsg['url'],None,True)
        if not permit:
            print("This site can't be reach!")
            continue
        httpmsg['url'] = url
        msg = changeurl(msg,url)
        if httpmsg['command'] == 'CONNECT':
            new_proxy_connection.send(b'HTTP/1.1 400 Fail \r\n\r\n')
            continue
        #if httpmsg['command'] == 'CONNECT':
        #    server_host, server_port = get_host_port(httpmsg['url'])
        #    server = create_client_socket(server_host, server_port)
        #    proxy_connection.send(returnestablish())
        #else:
        #if server == None:
        #    print("No connection")
        #
        #    continue
        #else:
        c = re.compile('.*:[0-9].*')
        if c.match(httpmsg['url']) is not None:
            server_host, server_port = get_host_port(httpmsg['url'])
        else:
            server_host = httpmsg['url']
            server_port = 80
        head_pat = re.compile(r'.*://')
        if head_pat.match(server_host):
            server_host = re.split(r'://',server_host)[-1]
        server_host = server_host.split(r'/')[0]
        print(server_host, server_port)
        server = create_client_socket(server_host, server_port)

        print("CP4")
        server.send(msg)
        print("CP5")

        recmsg = server.recv(65510)
        print("接收到的报文:")
        print(recmsg)
        new_proxy_connection.send(recmsg)
        mycache.add(msg, recmsg)

    except Exception as e:
        print(e)
        traceback.print_exc()
        break

if server is not None:
    server.close()

