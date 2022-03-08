import socket
import sys
import time

s=[]
PORT=14001
N=100
counter=0
ip=''

def _init(i):
    global s
    global ip
    try:
        s[i]=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except:
        print("Socket creation failed.")
        return False

    c=str(input("Type Y/N for localhot.\nTpye Q to Exit: ")).upper()
    while c!='Y' and c!='N' and c!='Q':
        c=str(input("Type Y/N for localhot.\nTpye Q to Exit: ")).upper()

    if c =='Y':
        host=socket.gethostbyname("localhost")
    elif c=='N':
        ip=str(input("Enter server IP: "))
        host=socket.gethostbyaddr(ip)[0]
    else:
        return False

    try:
        s[i].connect((host,PORT))
    except:
        print(host,"Port:"+str(PORT),"Unable to connect")

    s[i].send(bytes("25",'utf-8'))
    return True

def req_read(i,command):
    global s
    global counter

    try:
        s[i].send(bytes(command,'utf-8'))
    except:
        print("Reader"+str(i),"send operation error")
        return
    
    try:
        ans=str(s[i].recv(256),'utf-8')
        
    except:
        print("Server read results error")
        return
    counter+=1
    print("REPLY #"+str(counter)+":",ans)


s.append(0)
if  not(_init(0)):
    sys.exit(0)
c=str(input("Continuous send Y/N: ")).upper()    
com=str(input("Enter command: "))
if not(c=='Y'):
    for a in range(N):
        for i in range(N):
            req_read(0,com)
        time.sleep(0.5)
else:
    print("Continous ENABLED")
    while True:
        req_read(0,com)
        time.sleep(0.5)

for soc in s:
    soc.close()