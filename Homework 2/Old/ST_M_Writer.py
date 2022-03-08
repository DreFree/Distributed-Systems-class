import socket
import sys
import time

s=[]
PORT=14001
N=10
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

    s[i].send(bytes("31",'utf-8'))

def req_write(i,arr):
    global s
    global counter

    try:
        s[i].send(bytes(arr))
    except:
        print("Writer"+str(i),"send operation error")
        return
    counter+=1
    print("WROTE #"+str(counter),arr)

s.append(0)
_init(0)


for l in range(N):
    for i in range(N):
        a=[(lambda x: x*(l+1)+i)(x) for x in range(10)]
        req_write(0,a)
        time.sleep(0.02)
    time.sleep(5)

for soc in s:
    soc.close()
