#Half-duplex chat
#difference between HDuplex and FDuplex
#server
from socket import *
server_port=2000
server_socket=socket(AF_INET,SOCK_STREAM)
server_socket.bind(('',server_port))
server_socket.listen(1)
print("Welcome Chat is Ready")
print("Press 'q' to exit")
c_socket,adress=server_socket.accept()
while 1:
    sen=c_socket.recv(1024).decode()
    print(">>",sen)
    msg=input(">>")
    c_socket.send(msg.encode())
    if msg=='q':
        c_socket.close()
        break
        
    