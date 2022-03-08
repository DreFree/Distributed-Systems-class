import socket
import sys
import numpy as np
from threading import Lock,Event

SHUTDOWN=False
PORT=14001
Q=-1
s=0
READER=0
WRITER=0
ARR=np.full(10,-1,dtype=int)

lock=Lock()
event=Event()
def _init():
    global s
    global SHUTDOWN
    HOST=""
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except:
        print("Error creatimng socket")
        return False
    c=str(input("Type Y/N for localhost.\nType Q to quit: ")).upper()
    
    while c!='Q' and c!='N' and c!='Y':
        c=str(input("Type Y/N for localhost.\nType Q to quit: ")).upper()


    if c=='Y':
        HOST=socket.gethostbyname("localhost")
    elif c=='N':
        HOST=socket.gethostname()
    else:
        if s:
            s.close()
            SHUTDOWN=True
        return False
    try:
        s.bind((HOST,PORT))  
    except:
        print ("Error binding",HOST,"Port:"+str(PORT))
        return False

    return True
def _listen(s):
    global SHUTDOWN
    global READER
    global WRITER
    while True:
        if(SHUTDOWN):
            break
        (con, addr)=s.accept()
        buf=""
        try:
            buf=str(con.recv(2),"utf-8")
        except:
            print(addr[0],"Port:"+str(addr[1]),"Init read error")  
        
        if buf== "25":
            lock.acquire()
            READER+=1
            lock.release()
            if (WRITER==0):
                event.set()
            print("READER #"+str(READER),addr[0],"Port:"+str(addr[1]))
            reader(con,addr)
        elif buf=="31":
            lock.acquire()
            WRITER+=1
            lock.release()
            event.clear()
            print("WRITER #"+str(WRITER),addr[0],"Port:"+str(addr[1]))
            writer(con,addr)
        else:
            print(addr[0],"Port:"+str(addr[1]),"Invalid init params")
            con.close()
def operation(s):
    global ARR
    i=0
    ans=""
    while i <len(s):
        if s[i]!=" ":
            op=s[i]
            break
        i+=1

    if i==len(s):
        print("asdas")
        return "INCOMPLETE OPERATION"

    operand=s[i+1:]
    try:
        operand=int(operand)
    except:
        return "INCOMPLETE OPERAND"

    #print(op,operand)
    counter=0
    if op=='>':    
        for val in ARR:
            if int(val) > operand:
                counter+=1
                ans+=str(val)+' '
                
    else:
        ans+="INVALID"

    if counter>0:
        return ans
    else:
        return "NULL"

def reader(con,addr):
    global READER
    buf=""
    _error=False
    try:
        buf=str(con.recv(12).split(b'\0',1)[0],"utf-8")
    except:
        print("Reader",addr[0],"Port:"+str(addr[1]),"Read error1")
        _error=True
    
    try:
        if not(_error):
            con.send(bytes(operation(buf),'utf-8'))
    except:
        print("Reader",addr[0],"Port:"+str(addr[1]),"Send error1")
        _error=True
    
    event.wait()

    con.close
    lock.acquire()
    READER-=1
    lock.release()

def writer(con, addr):
    global WRITER
    global ARR
    buf=""
    try:
        buf=list(con.recv(1024))
    except:
        print("Sender",addr[0],"Port:"+str(addr[1]),"Read error1")
    
   
    con.close()
    lock.acquire()
    WRITER-=1
    ARR=buf
    lock.release()
    if (WRITER==0):
        event.set()

if not(_init()):
    sys.exit(1)
try:
    s.listen(Q)
except:
    print("Error on set listen param")
_listen(s)


print("HA")
s.close()