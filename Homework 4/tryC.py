import Pyro4
import sys

## simple python client to do RMI localhost
## without the use of Naming server ns


port=input("port: ")
try:
    obj=Pyro4.Proxy("PYRO:MyTest@localhost:"+str(port))
except Pyro4.errors.NamingError:
    print("Error locating Service")
    sys.exit(1)

try:
    result=obj.normal_method([10,20,30])
except Pyro4.errors.CommunicationError:
    print("Communication Error")
    sys.exit(1)

print(result)