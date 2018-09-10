class Decorator:
    def __init__(self,cls):
        self.cls = cls
    def __call__(self, *args, **kwargs):
        self.ins = self.cls(*args)
        return self
    def __getattr__(self, item):
        return getattr(self.ins,item)

class t1:
    def __init__(self,cls):
        self.cls = cls
        print 't1'
    def __call__(self, *args, **kwargs):
        self.ins = self.cls(*args)
        return self
class t2:
    def __init__(self,cls):
        self.cls = cls
        print 't2'
    def __call__(self, *args, **kwargs):
        self.ins = self.cls(*args)

class t3:
    def __init__(self,cls):
        self.cls = cls
        print 't3'
    def __call__(self, *args, **kwargs):
        self.ins = self.cls(*args)

@t1
@t2
@t3
class test:
    def __init__(self,name):
        self.name = name
    def pname(self):
        print self.name
test('bob')

def d1(func):
    return lambda :'d1' + func()
def d2(func):
    return lambda :'d2' + func()
def d3(func):
    return lambda :'d3' + func()
@d1
@d2
@d3
def function():
    return 'bob'

print (function())

