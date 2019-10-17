```
Title:   Python-build-in-super
Author:  Xiaoxue Wang<xxwjoy@hotmail.com>
Date:    2019-09-18
```

# python's built-in super()

`super([type[, object-or-type]])`
https://docs.python.org/3.7/library/functions.html#super

Diff `super()` & `super(FooBar, self)`.
And why `FooBar` & `self`?

**super: look for instance self's ancestor, starting point is FooBar.**

```python
class A:
    def method(self, arg):
        print("AAA")


class B(A):
    def method(self, arg):
        print("BBB")

class D(A):
    pass

class C(B):
    def method(self, arg):
        print("CCC")
        print("CCC self: ", self)
        super().method(arg)  # This does the same thing as super(C, self).method(arg)
        #super(C, self).method(arg)   # This will print CCC & BBB
        #super(B, self).method(arg)    # This will print CCC & AAA
        #super(D, self).method(arg)    # TypeError: self is not of D.

        # super(type, obj): obj must be an instance or subtype of type
        # type: is the starting point of the ansester looking.
        # In case super(B, self): it looking for B.__mro__, it's A. So ...

class E(C):
    pass

"""
>>> E.__mro__, C.__mro__, B.__mro__
((__main__.E, __main__.C, __main__.B, __main__.A, object),
 (__main__.C, __main__.B, __main__.A, object),
 (__main__.B, __main__.A, object))
>>>
>>> c = C()
>>> c.method("HI")
CCC
CCC self:  <__main__.C object at 0x7f3ce9d5fb50>
BBB
>>>
>>> e = E()
>>> e.method("HIE")
CCC
CCC self:  <__main__.E object at 0x7f3ce9df70d0>
BBB
"""
```

A more complicate example with MRO search :

```python
import collections
class LoggingDict(dict):
    def __setitem__(self, key, value):
        #logging.info('Setting %r to %r' % (key, value))
        print('Setting %r to %r' % (key, value))
        print("self: ", self, self.__repr__)
        print(super())
        # super().__setitem__(key, value)  # same as the below one
        super(LoggingDict, self).__setitem__(key, value)
        #dict.__setitem__(self, key, value)                     # LoggingDict instance call this
        #collections.OrderedDict.__setitem__(self, key, value)  # LoggingOD instance will call this


class LoggingOD(LoggingDict, collections.OrderedDict):
    pass

"""
>>> LoggingOD.__mro__, LoggingDict.__mro__, collections.OrderedDict.__mro__
((__main__.LoggingOD, __main__.LoggingDict, collections.OrderedDict, dict, object),
 (__main__.LoggingDict, dict, object),
 (collections.OrderedDict, dict, object))
>>>
>>> lg = LoggingDict()
>>> lg['a'] = 1
Setting 'a' to 1
self:  {} <method-wrapper '__repr__' of LoggingDict object at 0x7f3ce95bc1d0>
<super: <class 'LoggingDict'>, <LoggingDict object>>
>>> lg
{'a': 1}
>>>
>>> lod = LoggingOD()
>>> lod['a'] = 1
Setting 'a' to 1
self:  LoggingOD() <method-wrapper '__repr__' of LoggingOD object at 0x7f3ce9d31a70>
<super: <class 'LoggingDict'>, <LoggingOD object>>
>>> lod
LoggingOD([('a', 1)]))
"""
```

Since `LoggingOD.__mro__` , when call with `lod`,
`super(LoggingDict, self)` 's `self` is `LoggingOD()`.    
In `mro`, before `__main__.LoggingDict,` there are `collections.OrderedDict`, then `dict`.      
So, `collections.OrderedDict` is called here.

```
In [51]: LoggingOD.__mro__                                                                                           
Out[51]:
(__main__.LoggingOD,
 __main__.LoggingDict,
 collections.OrderedDict,
 dict,
 object)
```



**Refer to https://rhettinger.wordpress.com/2011/05/26/super-considered-super/**
