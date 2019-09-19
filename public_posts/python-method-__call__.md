```
Title:   Python-method-__call__
Author:  Xiaoxue Wang<xxwjoy@hotmail.com>
Date:    2019-09-19
```

## What is `__call__()` in python?

`object.__call__(self[, args...])` is for **Emulating callable objects**.

Called when the instance is “called” as a function;
if this method is defined, `x(arg1, arg2, ...)` is a shorthand for `x.__call__(arg1, arg2, ...)`.
(Note: a function is also an object.)
When a class have a `__call__` method, it call be called as a function.

```python
def func(x):
    print(f"Calling func {x} ...")
assert "__call__" in dir(func)

class Foo(object):
    def __init__(self, x):
        print(f"Foo __init__ with {x}.")
        self.x = x

class Bar(object):
    def __init__(self, x):
        print(f"Bar __init__ with {x}.")
        self.x = x

    def __call__(self, y):
        print(f"Bar __call__ with {y}.")
        self.y = y

"""
>>> fa = Foo(1)
Foo __init__ with 1.
>>> assert "__call__" not in dir(fa)
# fa()        # <-- TypeError: 'Foo' object is not callable
>>>
>>> ba = Bar(2)
Bar __init__ with 2.
>>> assert "__call__" in dir(ba)
>>> ba(6)
Bar __call__ with 6.
"""
```

Refer to https://docs.python.org/3/reference/datamodel.html#emulating-callable-objects
