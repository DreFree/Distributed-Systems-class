import socket
import time

ADDRESS = "192.168.0.163"
PORT = 14008
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = ["Mon", "Tue", "Wed", "Thu", "Fri"] # Data to send
for d in data:
    s.sendto(d.encode(), (ADDRESS, PORT)) # encode first
    print("Send: ", d)
    response, addr = s.recvfrom(1024)
    print("Receive %s from %s" % (response.decode(), addr))
    time.sleep(1)
