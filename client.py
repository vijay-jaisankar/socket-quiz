import socket
import select
import sys

# Setting up the socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Here the client is asked to input the script, ip address and port number
if len(sys.argv) != 3:
    print("Please enter in the following order :- <script> <IP> <port>")
    exit()


s.connect((str(sys.argv[1]), int(sys.argv[2])))

while True:

    
    list_of_sockets = [sys.stdin, s]	# Input Streams

    READ_sockets,WRITE_socket, ERROR_socket = select.select(list_of_sockets,[],[])	# Sockets to read,write and sockets

    for i in READ_sockets:
        if i == s:
            msg = i.recv(2048)
            print(msg)
        else:
            msg = sys.stdin.readline()
            s.send(msg)
            sys.stdout.flush()	# Very Important to flush the buffer


s.close()
sys.exit()
