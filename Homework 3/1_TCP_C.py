import socket
import time
HOST = '127.0.0.1' # The server's hostname or IP address
PORT = 65432 # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
data = ["Mon", "Tue", "Wed", "Thu", "Fri"] # Data to send
for d in data:
    s.sendall(d.encode("utf-8")) # encode before send
    print("Sent: ", d)
    time.sleep(1)
    response = s.recv(1024).decode("utf-8") # decode resp
    print('Received: ', response)
