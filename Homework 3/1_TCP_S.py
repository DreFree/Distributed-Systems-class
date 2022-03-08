import socket
HOST = '127.0.0.1' # Localhost
PORT = 65432 # Listening port
s = socket.socket(socket.AF_INET,
socket.SOCK_STREAM)
s.bind((HOST, PORT)) # bind the socket to the addr
s.listen(1) # listen to one conn at a time

while True:
    print('waiting for a connection')
    conn, addr = s.accept()
    try:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data) # echo
    finally:
    # Clean up the connection
        conn.close()