import socket
import struct
import sys
import time

multicast_group = ('224.3.29.72', 15001)
s=0
counter=0

def _init():    
    # Create the datagram socket
    global s
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except:
        print("Failed to created socket")
        return false

    ttl = struct.pack('b', 1)
    try:
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL,ttl)
    except:
        print("Failed to set up address for multi-cast")
    return True


def send_MC(msg):
    global s
    global multicast_group
    global counter
    counter+=1
    if counter>=5000:
        counter=0
    print("#"+str(counter),'sending "%s"' % msg)
    s.sendto(msg.encode(), multicast_group)

    


if not(_init()):
    if s:
        s.close()
    sys.exit(1)

l=['A','B','C','D','E','F','G','H','I','K']

c=str(input("Type Y/N for CONTINUOUS: ")).upper()

if c !='Y':
    for i in range(2):
        for letter in l:
            send_MC(letter)
            time.sleep(0.5)
else:
    while True:
        for letter in l:
            send_MC(letter)
            time.sleep(0.5)

s.close()

    