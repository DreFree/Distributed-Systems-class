import concurrent.futures
import socket
import select
import time
import struct
import sys

executor=0
MAX_WORKERS=15 +2
SHUTDOWN=False
s=0
PORT=14010
c=''


def _init():
    global s
    global c
    addr = (socket.gethostname(), PORT)
    c=str(input("Type U/T for UDP or TCP: ")).upper()
    while c!='U' and c!='T':
        c=str(input("Type U/T for UDP or TCP: ")).upper()

    if c=='U':    
        try:
            ##UDP Setup
            s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind(addr)
        except:
            print("Error create and bind socket")
            return False
    else:
        ##TCP setup
        try:
            s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(addr)
        except:
            print("Error create and bind socket")
            return False

    return True
def operation(data):
    ans=""
    temp=data.split(' ',3)
    if len(temp)<3:
        return "OPERATION INVALID"
    if temp[0]=='+':
        return str(int(temp[1])+int(temp[2]))
    elif temp[0]=='-':
        return str(int(temp[1])-int(temp[2]))
    elif temp[0]=='/':
        if int(temp[2])==0:
            return "DIV/0"
        return str(int(temp[1])/int(temp[2]))
    elif temp[0]=='*':
        return str(int(temp[1])*int(temp[2]))
    elif temp[0]=='-':
        return str(int(temp[1])-int(temp[2]))
    else:
        return "Unknown operation"

def listen_UDP():
    global s
    print("Waiting connection...")
    print("Server MODE: TCP Enabled")  
    while True:
        try:
            ready_to_read,ready_to_write,_in_error=select.select([s,],[s,],[])
        except select.error:
            print("Select error")
            break
        if len(ready_to_read)>0:    
            
            try:
                data, addr = s.recvfrom(1024)
                if not(data):
                    break
                data=data.decode('utf-8')
            except:
                print(addr[0],addr[1]," Error receiving data")
            else:
                executor.submit(send_UDP,data,addr)
                ##s.send(operation(data))

def send_UDP(data,addr):
    global SHUTDOWN
    print(addr[0],addr[1],':',data)
    if SHUTDOWN:
        return
    s.sendto(operation(data).encode(), addr)

def listen_TCP():
    global s
    global executor
    s.listen()
    print("Server MODE: TCP Enabled")
    print("Listening...")  
    while True:
        con,addr=s.accept()
        executor.submit(con_TCP,con,addr)

def con_TCP(con, addr):
    print(addr,"Connected")
    while True:
        try:
            ready_to_read,ready_to_write,in_error=select.select([con,],[con,],[])
        except select.error:
            con.shutdown(0)
            print(addr,"Error")
            break
        if SHUTDOWN:
            break
        
        if len(ready_to_read)>0:
            try:
                op=con.recv(1024)
            except:
                print(addr,"Error 2")
                break
            
            if not(op):
                print(addr,"Disconnected")
                break

            op=op.decode("utf-8")
            print(addr[0],addr[1],':',op)
            try:
                con.sendall(operation(op).encode())
            except:
                print(addr,"Send failed")
                break
    con.close()

def server_control():
    global s
    global executor
    global SHUTDOWN
    ans=str(input("Type Q to Exit:\n")).upper()
    while ans!='Q':
        ans=str(input("Type Q to Exit:\n")).upper()
    if ans=='Q':
        SHUTDOWN=True
        s.close()
        sys.exit(0)

if not(_init()):
    sys.exit(1)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)

if c=='U':
    executor.submit(listen_UDP)
else:
    executor.submit(listen_TCP)

server_control()

        


