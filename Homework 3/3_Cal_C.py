import socket
import sys
import time
import tkinter 

PORT=14010
SERVER='192.168.0.163'
s=0
c=''

def _init():
    global s
    global c
    c=str(input("Type U/T for UDP or TCP:\n")).upper()
    while c!='U' and c!='T':
        c=str(input("Type U/T for UDP or TCP:\n")).upper()

    if c=='U':
        print("Server MODE: UDP Enabled")    
        try:
            ##UDP Setup
            s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except:
            print("Error create socket")
            return False

    else:
        ##TCP setup
        print("Server MODE: TCP Enabled")  
        try:
            s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
        except:
            print("Error create socket")
            return False


        
        h=socket.gethostbyaddr(SERVER)
        ##h=socket.gethostname()
        try:
            s.connect((h[0],PORT))
        except:   
            print("Error connecting")
            return False

    return True

def send_UDP(msg,TO):
    global s
    print(msg)
    for i in range(10):
        s.sendto(msg.encode("utf-8"),TO)
        try:
            res , addr=s.recvfrom(1024)
        except:
            print("Server not responding..")
            break
        print(addr,':',res.decode('utf-8'))
        time.sleep(0.2)

def send_TCP(msg):
    global s
    global SERVER
    global PORT
    print (msg)
    for i in range(10):
        s.sendall(msg.encode("utf-8"))
        try:
            res=s.recv(1024)
        except:
            print("Server not responding...",i+1)
            break
        print((SERVER,PORT),':',res.decode('utf-8'))
        time.sleep(0.2)

if not(_init()):
    sys.exit(1)

c=str(input("Enter Comand :")).upper()
while c!='Q':
    if c=="U":
        send_UDP(c,(SERVER,PORT))
    else:
        send_TCP(c)
    c=str(input("Enter Comand :")).upper()


s.close()