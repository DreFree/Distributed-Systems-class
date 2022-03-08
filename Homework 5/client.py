import Pyro4
import sys

_nsEnable=True
choice=-1

SERVER=-1

d=str(input("NS active? Y/N: ")).upper()
while d!='Y' and d!='N':
    d=str(input("NS active? Y/N: ")).upper()

if d=='N':
    HOST=str(input("RMI server hostname: "))
    PORT=int(input("RMI server Port: "))

    try:        
        SERVER=Pyro4.Proxy(HOST+str(PORT))
    except Pyro4.errors.NamingError:
        print("Error locating RMI server.",HOST+str(PORT))

else:
    nsHOST=str(input("NS ip: "))
    nsPORT=int(input("NS port: "))
    try:
        ns=Pyro4.locateNS(host=nsHOST, port=nsPORT)

        
        while True:
            server_names = ns.list()
            if len(server_names)<=1:
                print("No Service registered with NS.\nType Q to Exit.\nPress ENTER to try again.")
                cho=str(input()).upper()
                if cho=='Q':
                    sys.exit()
            else:
                break

        keys=list(server_names.keys())
        print("Available server list:")
        counter=0
        for k in keys:
            if counter != 0:
                print(str(counter)+":",server_names[k])
            counter+=1

        choice=int(input("Enter number for above available server: "))
        while choice<1 or choice>=len(keys):
            choice=int(input("Enter number for above available server: "))
        key=keys[choice]
        print("Connected to:",server_names[key])
        try:
            SERVER=Pyro4.Proxy(server_names[key])
        except Pryo4.errors.NamingError:
            print("Unable to locate:",server_names[key])

    except Pyro4.errors.NamingError:
        print("Unable to locate NS")
        sys.exit(1)
print()
opt=input("Type S/R for Sender/Receiver mode: ").upper()
while opt !='S' and opt!='R':
    opt=input("Type S/R for Sender/Receiver mode: ").upper()

if opt =='S':
    print("SENDER MODE ENABLED")
    SID=int(input("Enter Sender ID: "))
    while True:
        print("Enter: ")
        print("1:- To register topic")
        print("2:- To Send message")
        print("3:- To delete a message")
        c=int(input())
        if c==1:
            topic=input("Enter Topic: ")
            print(SERVER.regis_by_name(topic,SID,True))
        elif c==2:
            topic=input("Enter Topic: ")
            msg=input("Enter msg: ")
            print(SERVER.send(SID,topic,msg))
        elif c==3:
            topic=input("Enter Topic: ")
            msg=input("Enter msg: ")
            msg_num=int(input("Enter mesage number: "))
            print(SERVER.delete(topic,SID,msg_num))
        else:
            print("Error in choice")
else:
    print("RECIEVER MODE ENABLED")
    RID=int(input("Enter Receiver ID: "))
    
    while True:
        check=SERVER.check(RID)
        if check:
            print(SERVER.recv(RID))
        print("\nEnter: ")
        print("1:- To register")
        print("2:- To check")
        print("3:- To recv")
        print("4:- To close")
        c=int(input())
        if c==1:
            topic=input("Enter Topic: ")
            print(SERVER.regis_by_name(topic,RID,False))
        elif c==2:
            if SERVER.check(RID):
                print("Pulling new messages...")
                print(SERVER.recv(RID))
            else:
                print("Up to date.")
        elif c==3:
            print(SERVER.recv(RID))
        elif c==4:
            break
        else:
            print("Error in choice")
