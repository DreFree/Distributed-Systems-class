import Pyro4
import time

##Simple RMI setup and registration for local host
##

def do_calculation(args):
    sum=0
    for arg in args:
        if True:
            sum+=int(arg)
    return sum


class MyClass(object):
    def __init__(self, nameserver,host="localhost",port=8000):
        self.host=host
        self.port=port
        self.nameserver=nameserver

    @Pyro4.expose
    def normal_method(self, args):
        time.sleep(10)
        result=do_calculation(args)
        return result

daemon=Pyro4.Daemon()
obj=MyClass("MyTest")
uri=daemon.register(obj,"MyTest")
print(uri)
print("Registration complete")
daemon.requestLoop()

