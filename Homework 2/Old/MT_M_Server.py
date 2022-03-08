import concurrent.futures
import socket
import sys
import numpy as np
from threading import Lock,Event,RLock

executor=0
MAX_WORKERS=10 +2
SHUTDOWN=False
PORT=14001
Q=-1
s=0
READER=0
WRITER=0
nw=0
nr=0

ARR=np.full(10,-1,dtype=int)
isARRset=False

lock=Lock()
lock1=RLock()
lock2=Rlock()
event=Event()

def _init(M):
    global s
    global SHUTDOWN
    global executor
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

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=M)
    return True
def _listen(s):
    global SHUTDOWN
    global READER
    global WRITER
    global executor
    print("Listening...")
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
            if WRITER==0:
                event.set()
            print("READER #"+str(READER),addr[0],"Port:"+str(addr[1]))
            executor.submit(reader,con,addr,READER)
        elif buf=="31":
            lock.acquire()
            WRITER+=1
            lock.release()
            event.clear()
            print("WRITER #"+str(WRITER),addr[0],"Port:"+str(addr[1]))
            executor.submit(writer,con,addr,WRITER)
        else:
            print(addr[0],"Port:"+str(addr[1]),"Invalid init params")
            con.close()
def operation(s):
    global ARR
    global isARRset
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

    if not(isARRset):
        return "ARRAY not initialized"

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

def reader(con,addr,num):
    global READER
    buf=""
    _error=False
    counter=0
    while True:
        try:            
            buf=str(con.recv(12).split(b'\0',1)[0],"utf-8")
        except:
            print("Reader",addr[0],"Port:"+str(addr[1]),"Read error1")
            _error=True

        if buf=="CLOSE":
            print("READER #"+str(num)+" DISCONNECT")
            break

        counter+=1
        print("READER #"+str(num)+" MES #"+str(counter)+":",buf)
        
        event.wait()

        try:
            if not(_error):
                con.send(bytes(operation(buf),'utf-8'))
                
        except:
            print("Reader",addr[0],"Port:"+str(addr[1]),"Send error1")
            _error=True

        if _error:
            break
    

    con.close
    lock.acquire()
    READER-=1
    lock.release()

def writer(con, addr,num):
    global WRITER
    global isARRset
    global ARR
    counter=0
    while True:

        buf=[]
        try:
            buf=list(con.recv(1024))
        except:
            print("Sender",addr[0],"Port:"+str(addr[1]),"Read error1")
            break
        
        if len(buf)==0:
            print("READER #"+str(num)+" DISCONNECT")
            break
              
        counter+=1
        print("WRITER #",str(num)," MSG #"+str(counter)+":",buf)
        write(buf)
        
        
        
        
        if WRITER==0:
            if not(event.isSet()):
                event.set()

    con.close()
    lock.acquire()
    WRITER-=1
    lock.release()

if not(_init(MAX_WORKERS)):
    sys.exit(1)
try:
    s.listen(Q)
except:
    print("Error on set listen param")

def write(arr):
    global nw
    global ARR
   
    if event.isSet():
        event.clear()
    
    nw+=1
    
    lock.acquire()
    ARR=arr
    lock.release()
    nw-=1
    if nw==0:
        if not(event.isSet()):
            event.set()
    
    
    

_listen(s)
print("HA")
s.close()