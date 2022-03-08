import socket
import sys
import time
from PyQt5 import sip

PORT=14010
SERVER='192.168.0.163'
s=0
c=''

def init_layout(self):
    top_layout = QGridLayout()
    top_layout.addWidget(self.movie_name_label, 0, 0)
    top_layout.addWidget(self.movie_name_line_edit, 0, 1)
    top_layout.addWidget(self.movie_source_label, 0, 2)
    top_layout.addWidget(self.movie_source_combobox, 0, 3)
    top_layout.addWidget(self.search_push_button, 0, 4)
    top_layout.addWidget(self.tip_label, 3, 1)
    top_layout.addWidget(self.search_content_label, 3, 0)
    top_layout.addWidget(self.search_content_text_list, 4, 0, 2, 5)

    main_frame = QWidget()
    self.setCentralWidget(main_frame)
    main_frame.setLayout(top_layout)

    ##self.reward_window = ImageWindow('resources/wechat_reward.jpg', '赞赏')
    ##self.watch_window = ImageWindow('resources/watch_wechat.jpg', '关注')

    return self 

def _init():
    global s
    global c
    c=str(input("Type U/T for UDP or TCP:\n")).upper()
    while c!='U' and c!='T':
        c=str(input("Type U/T for UDP or TCP:\n")).upper()

    if c=='U':
        print("Server MODE: UDP Enabled")    
        try:
            ##UDP Setup
            s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except:
            print("Error create socket")
            return False

    else:
        ##TCP setup
        print("Server MODE: TCP Enabled")  
        try:
            s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
        except:
            print("Error create socket")
            return False


        
        h=socket.gethostbyaddr(SERVER)
        ##h=socket.gethostname()
        try:
            s.connect((h[0],PORT))
        except:   
            print("Error connecting")
            return False

    return True

def send_UDP(msg,TO):
    global s
    print(msg)
    for i in range(10):
        s.sendto(msg.encode("utf-8"),TO)
        try:
            res , addr=s.recvfrom(1024)
        except:
            print("Server not responding..")
            break
        print(addr,':',res.decode('utf-8'))
        time.sleep(0.2)

def send_TCP(msg):
    global s
    global SERVER
    global PORT
    print (msg)
    for i in range(10):
        s.sendall(msg.encode("utf-8"))
        try:
            res=s.recv(1024)
        except:
            print("Server not responding...",i+1)
            break
        print((SERVER,PORT),':',res.decode('utf-8'))
        time.sleep(0.2)

if not(_init()):
    sys.exit(1)

init_layout()
c=str(input("Enter Comand :")).upper()
while c!='Q':
    if c=="U":
        send_UDP("+ 4 5",(SERVER,PORT))
    else:
        send_TCP("+ 4 5")
    c=str(input("Enter Comand :")).upper()