## @file
## pure Python -> C metaprogramming sample

import os

## metatprogramming elements
class Meta:
    def __init__(self,V):
        ## type/class tag
        self.tag = self.__class__.__name__.lower()
        ## single value
        self.val = V
        ## `attr{}`ibutes /associative/
        self.attr = {}
        ## `nest[]`ed elements /ordered/
        self.nest = []
    def __repr__(self): return self.dump()
    def dump(self,depth=0):
        S = self.pad(depth) + self.head()
        for i in self.attr:
            S += self.pad(depth+1) + self.attr[i].head(prefix='%s = '%i)
        for j in self.nest:
            S += j.dump(depth+1)
        return S
    def pad(self,N):
        return '\n'+'\t'*N
    def head(self,prefix=''):
        return '%s<%s:%s>'%(prefix,self.tag,self.val)
    def __setitem__(self,K,o):
        self.attr[K] = o ; return self

## primitive elements        
class Primitive(Meta): pass

## string
class Str(Primitive): pass 
        
## variable
class Var(Meta): pass
    
## directory
class Dir(Meta):
    def __init__(self,V):
        Meta.__init__(self, V)
        try: os.mkdir(V)
        except OSError: pass
    def __lshift__(self,o):
        return File(self.val+'/'+o)

## file
class File(Meta):
    def __init__(self,V):
        Meta.__init__(self, V)
        self.fh = None
    def __lshift__(self,o):
        if type(o) == type(''):
            self.nest.append(Str(o))
        else:
            self.nest.append(o)
        return self
    def write(self):
        F = open(self.val,'w')
        F.close()
    
class MakeVar(Var):
    pass
 
## software module
class Module(Meta):
    ## construct empty module
    def __init__(self,V):
        Meta.__init__(self, V)
        self['dir'] = self.dir = Dir(V)
        self.mk = self.dir << 'Makefile'
         
## C++ Module
class CppModule(Module):
    ## construct module
    def __init__(self,V):
        Module.__init__(self, V)
        self.exe = self.dir << '%s.exe'%V
        self.hpp = self.dir << '%s.hpp'%V
        self.cpp = self.dir << '%s.cpp'%V
        self.mk << self.exe.val << ': $(C) $(H)'
 
## hello world application
hello = CppModule('hello')
print hello.mk
