import socket
import sys
import time

s=[]
PORT=14001
N=20
counter=0

def _init(i):
    global s
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
        host=socket.gethostname()
    else:
        return False

    try:
        s[i].connect((host,PORT))
    except:
        print(host,"Port:"+str(PORT),"Unable to connect")

    s[i].send(bytes("25",'utf-8'))

def req_read(i):
    global s
    global counter

    try:
        s[i].send(bytes(">10",'utf-8'))
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
_init(0)
for a in range(N):
    for i in range(N):
        req_read(0)
    time.sleep(5)
for soc in s:
    soc.close()