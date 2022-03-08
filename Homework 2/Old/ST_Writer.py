import socket
import sys

s=[]
PORT=14001

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
    
    try:
        s[i].send(bytes(arr))
    except:
        print("Writer"+str(i),"send operation error")
        return


s.append(0)
_init(0)
a=[(lambda x: x*2)(x) for x in range(10)]
req_write(0,a)