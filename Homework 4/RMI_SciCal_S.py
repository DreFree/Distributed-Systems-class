import Pyro4
import socket
import math

SERVICE="Sci-Cal"

@Pyro4.expose
class SciCal (object):
    def __init__(self):
        pass
    def add (self,a,b):
        return a+b

    def sub (self,a,b):
        return a-b

    def mul (self,a,b):
        return a*b
    
    def div (self,a,b):
        if b==0:
            return "DIV/0"
        return a/b

    def pow(self,a,b):
        return pow(a,b)

    def sqr(self,a):
        return math.sqrt(a)
    
    def log (self,a, b=10):
        return math.log(a,b)
    
    def sin(self,a):
        return math.sin(a)

    def cos(self,a):
        return math.cos(a)

c=input("NS active Y/N: ").upper()
while c!='N' and c!='Y':
    c=input("NS active Y/N: ").upper()
    
daemon=Pyro4.core.Daemon(host=socket.gethostname())
obj=SciCal()
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