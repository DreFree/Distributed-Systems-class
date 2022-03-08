import socket
HOST = '127.0.0.1' # localhost
PORT = 6789 # Port send to
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
while True:
    print('Waiting to receive...')
    data, addr = s.recvfrom(1024)
    print("recvfrom %s and echo %s" % (addr, data))
    s.sendto(data, addr)
