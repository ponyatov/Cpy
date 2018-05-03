class Object:
    def __init__(self,V):
        self.val = V

class Active(Object):
    pass

class Meta(Active):
    pass

class Module(Meta):
    def __init__(self,V): Meta(V)
    
hello = Module('hello')
print hello
