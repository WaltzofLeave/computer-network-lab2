import socket
def create_server_socket(host,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ip_port = (host, port)
    s.bind(ip_port)
    s.listen(50)
    return s
connectedmsg = b'HTTP/1.1 200 Connection Established'
proxy_user_socket = create_server_socket('127.0.0.1', 10005)
while True:
    new_proxy_user_socket, address = proxy_user_socket.accept()
    msg = new_proxy_user_socket.recv(60000)
    print(msg.decode('utf-8'))
