import socket
import select
import time
import struct
import sys

s=0
PORT=15001
multicast_group='224.3.29.72'
SHUTDOWN=False

def _init():
    global s
    global multicast_group
    global PORT
    
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except:
        print("Error setting up socket")
        return False

    addr = (socket.gethostname(), PORT)
    try:
        s.bind(addr)
        print("Multicast bind complete.")
    except:
        print("Error binding")


    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    try:
        s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    except:
        print("Error multicast add membership")
        return False
    
    return True
def listen():
    global s
    print("Awaiting broadcast...")
    while True:
        if SHUTDOWN:
            break
        try:
            ready_to_read, ready_to_write,_inerror=select.select([s,],[s,],[])
        except select.error:
            print("Select error")
        else:
            if len(ready_to_read) >0:
                try:
                    data, address = s.recvfrom(1024)
                except:
                    print("Read Error")
                else:    
                    if data:
                        print("Received: ",data.decode("utf-8"))
    s.close()    
        

if not(_init()):
    if s:
        s.close()
    sys.exit(1)
listen()