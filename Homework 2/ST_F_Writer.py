import socket
import sys
import time

s=[]
PORT=14001
N=10
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

    s[i].send(bytes("31",'utf-8'))

    return True

def req_write(i,arr):
    global s
    global counter

    counter+=1

    try:
        s[i].sendall(bytes(arr))
    except:
        print("Writer"+str(i),"send operation error")
        return

    print("Writing #"+str(counter),arr)

    try:
        res=str(s[i].recv(12),'utf-8')
        if res=="ACK":
            print("Write complete")
    except:
        print("Writer"+str(i),"No ACK")
    
    
    

s.append(0)
if not(_init(0)):
    sys.exit(0)
c=str(input("Continuous send Y/N: ")).upper()
num=int(input("Sequence start point: "))
if not(c=='Y'):
    for i in range(N):
        a=[(lambda x: (x)+num+i)(x) for x in range(10)]
        req_write(0,a)
        time.sleep(7.0)
else:
    print("Continuous ENABLED")
    i=0
    while True:
        if i+num >=245:
            i=0
            num=0
        a=[(lambda x: (x)+num+i)(x) for x in range(10)]
        req_write(0,a)
        time.sleep(7.0)
        i+=1
        

for soc in s:
    soc.close()
