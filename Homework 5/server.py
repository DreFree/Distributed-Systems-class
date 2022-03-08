import Pyro4
import socket
import math
import sys

SERVICE="MessageBoard"
offset_start_at=0

class Message_Board(object):
    def __init__ (self):
        self.topic_name=[]
        self.topic_msg=[[]]
        self.topic_sender=[[]]
        self.topic_receiver=[[]]
        self.topic_reciever_offset=[[]]
        self.istesting=True
        if self.istesting:
            ##self.test()
            pass
        

    def test(self):
        self.print_state()
        self.regis_by_name("drugs",101,True)        
        self.regis_by_name("drugs",1012,True)
        self.regis_by_name("cars",22,True)
        self.regis_by_name("pig",231,False)
        self.regis_by_name("asdadads",333,False)
        self.regis_by_name("drugs",333,False)
        self.regis_by_name("drugs",345,False)      
        self.regis_by_name("dog",997,True)
        self.regis_by_name("dog",544,True)
        self.regis_by_name("dog",231,False)
        self.regis_by_name("cars",231,False)
        self.send(9999,"cars","Hello world")
        self.send(22,"cars","Hello world")
        self.send(22,"cars","YOUR MAMA")
        print("check:",self.check(231))
        self.recv(231)
        print("check:",self.check(231))
        self.recv(333)
        print()

        print(self.delete("cars",22,1))
        
        return

    @Pyro4.expose
    def regis_by_name (self,name,id,isSender):
        global offset_start_at
        for i,_name in enumerate(self.topic_name):
            if _name==name:
                if isSender:
                    self.topic_sender[i].append(id)
                else:
                    self.topic_receiver[i].append(id)
                    self.topic_reciever_offset[i].append(offset_start_at)
                if self.istesting:
                    self.print_state()
                return "SUCCESSFUL Registration to existing topic"
        if isSender:
            if len(self.topic_name)==0:
                self.topic_name.append(name)
                self.topic_sender[0].append(id)
            else:
                self.topic_name.append(name)
                self.topic_sender.append([id])
                self.topic_receiver.append([])
                self.topic_reciever_offset.append([])
                self.topic_msg.append([])
            if self.istesting:
                self.print_state()
            return "SUCCESSFUL new topic registration"
        else:
            return "Topic not on Board"

    @Pyro4.expose
    def send (self,id,topic,msg):
        _tid=self.get_id_pos(self.topic_name,topic)
        if _tid>=0:
            if id in self.topic_sender[_tid]:
                self.topic_msg[_tid].append(msg)
                if self.istesting:
                    self.print_state()
                return "Message Sent"
            else:
                return "Sender ID not registered to this topic"
        else:
            return "Topic id not found"
    @Pyro4.expose
    def recv (self,id):
        msg=[]
        for i,L in enumerate(self.topic_receiver):
            for j,I in enumerate(L):
                if I == id:
                    temp=[self.topic_name[i]]
                    temp2=self.topic_msg[i][self.topic_reciever_offset[i][j]:]
                    l=len(temp2)
                    temp.append(temp2)
                    msg.append(temp)
                    self.topic_reciever_offset[i][j]+=l
        if self.istesting:
            self.print_state()
            print(msg)           
        return msg

    @Pyro4.expose
    def delete(self,tid,id,msg_num):
        msg_num-=1
        _tid=self.get_id_pos(self.topic_name,tid)
        if _tid>=0:
            _mid=self.get_id_pos(self.topic_sender[_tid],id)
            if _mid >=0:
                if len(self.topic_msg[_tid]) >msg_num:
                    self.topic_msg[_tid].pop(msg_num)             #remove(self.topic_msg[_tid][msg_num])
                    self.offset_readjust(_tid,msg_num)
                    if self.istesting:
                        self.print_state()
                    return "Message successfully deleted"
                else:
                    return "Message list not that long"
            else:
                return "Not a registered Sender for this topic"
        return "Topic Selection doesnt exist"
    
    @Pyro4.expose
    def check(self,id):
        for i, L in enumerate(self.topic_receiver):
            for j, P in enumerate(L):
                if P == id:
                    #print(P)
                    #print(len(self.topic_msg[i]))
                    if self.topic_reciever_offset[i][j]<len(self.topic_msg[i]):
                        return True
        
        return False


    def offset_readjust(self,tid,num):
        for i, off in enumerate(self.topic_reciever_offset[tid]):
            if off>= num:
                self.topic_reciever_offset[tid][i]-=1
        return
    def get_id_pos (self,L,id):
        for i,item in enumerate(L):
            if item == id:
                return i
        return -1

    def print_state(self):
        print("Topic:   ",self.topic_name)
        print("Sender:  ",self.topic_sender)
        print("Receiver:",self.topic_receiver)
        print("Offset:  ",self.topic_reciever_offset)
        print("MSG:     ",self.topic_msg)
        print()
        return

c=input("Type Q to EXIT.\nNS active Y/N: ").upper()
while c!='N' and c!='Y' and c!='Q':
    c=input("Type Q to EXIT.\nNS active Y/N: ").upper()

obj=Message_Board()
if c=='Q':
    sys.exit(0)

daemon=Pyro4.core.Daemon(host=socket.gethostname())

try:
    uri=daemon.register(obj,SERVICE)
except:
    print ("Daemon registration failed")
    sys.exit(1)

print("URI:",uri)

if c=='Y':
    HOST=input("NameServer IP: ")
    PORT=int(input("NameServer Port: "))
    try:
        ns = Pyro4.locateNS(host=HOST,port=PORT)
    except Pyro4.errors.NamingError:
        print("Unable to locate NS")

    ns.register(SERVICE,uri)
    print("NS registration complete")

daemon.requestLoop()