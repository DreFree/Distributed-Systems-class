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

while True:
    print("Enter: ")
    print("1:- Add")
    print("2:- Sub")
    print("3:- Mul")
    print("4:- Div")
    print("5:- Pow")
    print("6:- Sqr")
    print("7:- Log")
    print("8:- Sin")
    print("9:- Cos")
    print ("0:- To exit")

    c=int(input())
    if c==0:
        break
    if c==1:
        a=int(input("Num1: "))
        b=int(input("Num2: "))
        print("ANS:",SERVER.add(a,b))
    elif c==2:
        a=int(input("Num1: "))
        b=int(input("Num2: "))
        print("ANS:",SERVER.sub(a,b))
    elif c==3:
        a=int(input("Num1: "))
        b=int(input("Num2: "))
        print("ANS:",SERVER.mul(a,b))
    elif c==4:
        a=int(input("Num1: "))
        b=int(input("Num2: "))
        while b==0:
            b=int(input("Cant Div by 0.\nNum2: "))
        print("ANS:",SERVER.div(a,b))
    elif c==5:
        a=int(input("Num1: "))
        b=int(input("Num2: "))
        print("ANS:",SERVER.pow(a,b))
    elif c==6:
        a=int(input("Num1: "))
        print("ANS:",SERVER.sqr(a))
    elif c==7:
        a=int(input("Num1: "))
        b=int(input("Num2: "))
        print("ANS:",SERVER.log(a,b))
    elif c==8:
        a=int(input("Num1: "))
        print("ANS:",SERVER.sin(a))
    elif c==9:
        a=int(input("Num1: "))
        print("ANS:",SERVER.cos(a))
    else:
        print("Error in choice")