```
Title:   Understand-Python-Decorator-with-Examples
Author:  Xiaoxue Wang<xxwjoy@hotmail.com>
Versions:
    - 2019-08-14: newly created, 2.5 hours taken
```

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->
<!-- code_chunk_output -->

- [ Understand Python Decorator with Examples](#understand-python-decorator-with-examples)
  - [ Start with an usecase](#start-with-an-usecase)
    - [ Usecase: 2 functions with same header & footer](#usecase-2-functions-with-same-header-footer)
    - [ How to reuse the header & footer part among functions?](#how-to-reuse-the-header-footer-part-among-functions)
    - [ Can we make the `func1`/`func1_2` not called by `log1` directly? We want to call it as our need.](#can-we-make-the-func1func1_2-not-called-by-log1-directly-we-want-to-call-it-as-our-need)
    - [ Good! Let's see how python's decorator grammar sugar works here ...](#good-lets-see-how-pythons-decorator-grammar-sugar-works-here)
  - [ More cases/requires in python's decorator](#more-casesrequires-in-pythons-decorator)
    - [ (inner parameters) What if we need a func3 with parameters ?](#inner-parameters-what-if-we-need-a-func3-with-parameters)
    - [ (outer parameters) What if we want the `log` to be more flexible by adding parameters ?](#outer-parameters-what-if-we-want-the-log-to-be-more-flexible-by-adding-parameters)
      - [ A try without `@` usage, we use plain functions](#a-try-without-usage-we-use-plain-functions)
      - [ Try with `@` ...](#try-with)
      - [ Learn from last failure, Retry with `@` ... WORK!](#learn-from-last-failure-retry-with-work)
    - [ (outer&inner parameters) Let both the decorator and be decorated functions have parameters.](#outerinner-parameters-let-both-the-decorator-and-be-decorated-functions-have-parameters)
  - [ What is it like: Multiple levels of decorator for a function](#what-is-it-like-multiple-levels-of-decorator-for-a-function)
  - [ What is it like: to decorate a class?](#what-is-it-like-to-decorate-a-class)
  - [ What is it like: the decorator is a class?](#what-is-it-like-the-decorator-is-a-class)
  - [ [TOADD] What is it like: both the decorator and to decorated are classes?](#toadd-what-is-it-like-both-the-decorator-and-to-decorated-are-classes)

<!-- /code_chunk_output -->



# Understand Python Decorator with Examples

Note: See examples in jupyter-notebook format in file `./underdtand-decorator-with-examples.ipynb`

## Start with an usecase
### Usecase: 2 functions with same header & footer

```python
def func1():
    print('entering')

    for i in range(3):
        print(i)

    print('exiting')

func1()
print("-------------------")
def func2():
    print('entering')

    for i in range(5):
        print(i)

    print('exiting')

func2()

# ===========================================
# Output:
"""
entering
0
1
2
exiting
-------------------
entering
0
1
2
3
4
exiting
"""
```


### How to reuse the header & footer part among functions?

Put the header & footer into a function, to make it reusable.

```python
# v1
def log1(func):
    ''' Used for header & footer purpose. Call function func in between.'''
    print('entering')
    func()               # <-- func is called inside the log1, when log1 is called.
    print('exiting')
    # The return value of log1 is None.

def func1():
    for i in range(3):
        print(i)

def func1_2():
    for i in range(2):
        print(i)

v1 = log1(func1)
print("-------")
print('v1: ', v1)

print("-------------------")

v1_2 = log1(func1_2)
print("-------")
print('v1_2: ', v1_2)

# ===========================================
# Output:
"""
entering
0
1
2
exiting
-------
v1:  None
-------------------
entering
0
1
exiting
-------
v1_2:  None
"""
```

### Can we make the `func1`/`func1_2` not called by `log1` directly? We want to call it as our need.

Still not good enough, when `log1` is called, the parameter `func1` is also called inside  `log1`. Can we make the `func1`/`func1_2` not called by `log1`, until we call it directly?

The improvements here:
Change the `log2`.
Inside `log2`, wrap the old content of function `log1`(include calling of `func()`) into a temporary function, named `inner` here.
When `log2` is called with `f2 = log2(func2)`,
`f2` is assigned with function `inner`.
Calling `f2` as you need then.

```python
# v2    
def log2(func):
    print("Step in first-level of log2")
    def inner():
        print('entering')
        func()    
        print('exiting')
    print("Exiting of first-level of log2")
    return inner                # <-- The return value of log2 is function inner .
                                # <-- Hence, log2 is a high-level function.

def func2():
    for i in range(5):
        print(i)

f2 = log2(func2)

print("-------------------")
print('f2: ', f2)
print("-------------------")
f2()                             # <-- func2 is called at this moment.

# ===========================================
# Output:
"""
Step in first-level of log2
Exiting of first-level of log2
-------------------
f2:  <function log2.<locals>.inner at 0x7fae9851d400>
-------------------
entering
0
1
2
3
4
exiting
"""
```

### Good! Let's see how python's decorator grammar sugar works here ...

The `@log3` will do the calling of `log3(func3)`, and assign the return value of `log3(func3)` to `func3`.
Later after this definition, when calling `func3` equals calling `log3`'s `inner` with the original `func3`'s body as parameter.

```python
# v3
def log3(func):                 # <-- same as log2
    print("Step in first-level of log3")
    def inner():
        print('entering')
        func()    
        print('exiting')
    print("Exiting of first-level of log3")
    return inner

@log3                           # <-- grammar sugar: do the calling of `log3(func3)`.
def func3():
    for i in range(2):
        print(i)

print("-------------------")
print('func3: ', func3)
print("-------------------")
func3()

# ===========================================
# Output:
"""
Step in first-level of log3
Exiting of first-level of log3
-------------------
func3:  <function log3.<locals>.inner at 0x7fae9810eea0>
-------------------
entering
0
1
exiting
"""
```

## More cases/requires in python's decorator
### (inner parameters) What if we need a func3 with parameters ?

No big difference here.
Since `func3` need parameters, ok, just add same parameters to `inner` for wrapping. Make them consist. (`inner` is just a wrapping. Basically, it doesn't need to handle the parameters for `func3` at all.)

```python
# v2

def log3(func):
    print("Step in first-level of log")
    def inner(x):
        print('entering')
        func(x)    
        print('exiting')
    print("Exiting of first-level of log")
    return inner


@log3
def func3(x):
    print("DEBUG: fun3 accept param: ", x)
    for i in range(x):
        print(i)

print("-------------------")
print('func3: ', func3)
print("-------------------")
func3(2)
# ===========================================
# Output:
"""
Step in first-level of log
Exiting of first-level of log
-------------------
func3:  <function log3.<locals>.inner at 0x7fae8a635ea0>
-------------------
entering
DEBUG: fun3 accept param:  2
0
1
exiting
"""
```


### (outer parameters) What if we want the `log` to be more flexible by adding parameters ?

#### A try without `@` usage, we use plain functions
```python
# v1

def log1(msg, func):                   # <-- log1 must accept 2 params together.
    print("Step in first-level of log")
    def inner():
        print('entering')
        print(msg)                     # <-- this `msg` variable is passed into inner() inexplicitly.
        func()    
        print('exiting')
    print("Exiting of first-level of log")
    return inner

def func1():
    print("DEBUG: Run into fun1 ...")
    for i in range(2):
        print(i)

f1 = log1('MSG: Hi', func1, )

print("-------------------")
print('f1: ', f1)
print("-------------------")
f1()
# ===========================================
# Output:
"""
Step in first-level of log
Exiting of first-level of log
-------------------
f1:  <function log1.<locals>.inner at 0x7f47fcd56400>
-------------------
entering
MSG: Hi
DEBUG: Run into fun1 ...
0
1
exiting
"""
```

#### Try with `@` ...
An explicitly trying direction, we add parameters to `log`'s definition,
then when `@log1("MSG: Hi")` with `def func1():`,
it will equals to `log1("MSG: Hi", func1)`.
(**BUT,** this guessing is not right at all. See the Output of below examples.)


```python
# v1
def log1(*args, **kwargs):  
    # Guessing: this args should == (msg, func).
    print("*args, **kwargs: ", args, kwargs)
    print("Step in first-level of log")
    def inner(*inargs, **inkwargs):
        # Guessing: this inargs should be empty.
        print("*inargs, **inkwargs: ", inargs, inkwargs)
        print('entering')
        #print(msg)  
        #func()    
        print('exiting')
    print("Exiting of first-level of log")
    return inner

@log1("MSG: Hi")
def func1():
    print("DEBUG: Run into fun1 ...")
    for i in range(2):
        print(i)

print("-------------------")
print('func1: ', func1)
print("-------------------")
#func1()

# ===========================================
# Output:
"""
*args, **kwargs:  ('MSG: Hi',) {}
Step in first-level of log
Exiting of first-level of log
*inargs, **inkwargs:  (<function func1 at 0x7f47fced5730>,) {}
entering
exiting
-------------------
func1:  None
-------------------
"""
```

#### Learn from last failure, Retry with `@` ... WORK!

Let's learn from the last output.
Actually, `log1` is called like `log1("MSG: Hi")` then `inner(func1)`, add them together, we get `log1("MSG: Hi")(func1)`,.
If so, to keep the `inner` still be as the simple wrapper for `func1`,
one more wrapping level should be involved to handle the `@` leading 2-level-calling, eg `log1("MSG: Hi")(func1)`.

Adding a `wrap` here ...

```python
# v4

def log4(msg):                   # <-- accept @log4's parameters
    print("Step in first-level of log")        
    def wrap(func):              # <-- accept the decorated function
        print("Step in second-level of log")
        def inner():
            print('entering')
            print(msg)
            func()    
            print('exiting')
        print("Exiting of second-level of log")
        return inner
    print("Exiting of first-level of log")
    return  wrap


@log4('MSG: HI')
def func4():
    print("DEBUG: Run into func4 ...")
    for i in range(3):
        print(i)

print("-------------------")
print('func4: ', func4)
print("-------------------")
func4()

print("===================")

# ===========================================
# Output:
"""
Step in first-level of log
Exiting of first-level of log
Step in second-level of log
Exiting of second-level of log
-------------------
func4:  <function log4.<locals>.wrap.<locals>.inner at 0x7f47fcfbbf28>
-------------------
entering
MSG: HI
DEBUG: Run into func4 ...
0
1
2
exiting
===================
"""
```

### (outer&inner parameters) Let both the decorator and be decorated functions have parameters.

```python
# v5

def log5(msg):                   # <-- accept @log4's parameters
    print("Step in first-level of log")        
    def wrap(func):              # <-- accept the decorated function
        print("Step in second-level of log")
        def inner(x):            # <-- accept the decorated function's parameters
            print('entering')
            print(msg)
            func(x)    
            print('exiting')
        print("Exiting of second-level of log")
        return inner
    print("Exiting of first-level of log")
    return  wrap


@log5('MSG: HI')
def func5(x):
    print("DEBUG: Run into func5 ...")
    for i in range(x):
        print(i)

print("-------------------")
print('func5: ', func5)
print("-------------------")
func5(2)
print("===================")

# ===========================================
# Output:
"""
Step in first-level of log
Exiting of first-level of log
Step in second-level of log
Exiting of second-level of log
-------------------
func5:  <function log5.<locals>.wrap.<locals>.inner at 0x7f47fcee1d08>
-------------------
entering
MSG: HI
DEBUG: Run into func5 ...
0
1
exiting
===================
"""
```

## What is it like: Multiple levels of decorator for a function

See this example first, and we read from the output.

```python
def add_tag(tag):
    print("Step into add_tag with : ", tag)
    def dec(fn):
        print("Step into dec with : ", fn)
        def wrap(name):
            return '<' + tag + '>' + fn(name) + '</' + tag + '>'
        print("Step out of dec, returning : ", wrap)
        return wrap
    print("Step out of add_tag, returning : ", dec)
    return dec

@add_tag('i')                  # <-- calling `add_tag('i')( add_tag('p')(hello) )
@add_tag('p')                  # <-- What's the calling combination and order here ???
def hello(i):
    return 'hello ' + i

print("-------------------")
print('hello: ', hello)
print("-------------------")
tmp = hello('world')         # <-- add_tag('i')(add_tag('p')(hello))('world')
print("-------------------")
print(tmp)

# ===========================================
# Output:
"""
Step into add_tag with :  i
Step out of add_tag, returning :  <function add_tag.<locals>.dec at 0x7f47fcee1bf8>
Step into add_tag with :  p
Step out of add_tag, returning :  <function add_tag.<locals>.dec at 0x7f48040cf510>
Step into dec with :  <function hello at 0x7f47fcd56ea0>
Step out of dec, returning :  <function add_tag.<locals>.dec.<locals>.wrap at 0x7f47fcd56bf8>
Step into dec with :  <function add_tag.<locals>.dec.<locals>.wrap at 0x7f47fcd56bf8>
Step out of dec, returning :  <function add_tag.<locals>.dec.<locals>.wrap at 0x7f47fcd56730>
-------------------
hello:  <function add_tag.<locals>.dec.<locals>.wrap at 0x7f47fcd56730>
-------------------
-------------------
<i><p>hello world</p></i>
"""
```

From the ouput, the 2-layer of `@add_tag` are called like:

```
calling             return
-------------       --------
add_tag('i')  -->   dec_i
add_tag('p')  -->   dec_p
dec_p(hello)  -->   wrap_p
dec_i(wrap_p) -->   wrap_p_i

==> hello := wrap_p_i

hello('world')  -->  wrap_p_i('world')
==> <i><p>hello world</p></i>
```
The `add_tag` related 4 callings are added up to: `add_tag('i')( add_tag('p')(hello) )` .


## What is it like: to decorate a class?

Still, in this below example, `MyClass` is assigned to function `getinstance`. :D
Same as what we know for functions.

```python
# https://www.python.org/dev/peps/pep-0318/#examples
# Example 2:

def singleton(cls):
    print("Step into singleton ...")
    print("param cls: ", cls)
    instances = {}
    def getinstance():
        print("Step into getinstance ...")
        if cls not in instances:
            instances[cls] = cls()
        print("Step out getinstance ...")
        return instances[cls]
    print("Step out singleton ...")
    return getinstance

@singleton
class MyClass:
    print("Class MyClass")
    def __init__(self):
        print("MyClass's __init__ ...")

print("-------------------")
print(MyClass)
print("-------------------")
mc1 = MyClass()
print("-------------------")
mc2 = MyClass()
print("-------------------")
print("mc1, mc2: ", mc1, mc2)
print("-------------------")
print("mc1, mc2: ", mc1, mc2)
print("-------------------")

# ===========================================
# Output:
"""
Class MyClass
Step into singleton ...
param cls:  <class '__main__.MyClass'>
Step out singleton ...
-------------------
<function singleton.<locals>.getinstance at 0x7f664cf70598>
-------------------
Step into getinstance ...
MyClass's __init__ ...
Step out getinstance ...
-------------------
Step into getinstance ...
Step out getinstance ...
-------------------
mc1, mc2:  <__main__.MyClass object at 0x7f664c710208> <__main__.MyClass object at 0x7f664c710208>
-------------------
mc1, mc2:  <__main__.MyClass object at 0x7f664c710208> <__main__.MyClass object at 0x7f664c710208>
-------------------
"""
```

## What is it like: the decorator is a class?

In below example, `@add_tag('p')` will `add_tag.__init__('p')`, then `add_tag.__call__(hello)` .

```python
class add_tag(object):
    def __init__(self, tag):
        print("init add_tag with : ", tag)
        self.tag = tag

    def __call__(self, fn):
        print("call add_tag with : ", fn)
        def wrap(name):
            return '<' + self.tag + '>' + fn(name) + '</' + self.tag + '>'
        return wrap

@add_tag('p')
def hello(i):
    return 'hello ' + i

print("-------------------")
print('hello: ', hello)
print("-------------------")
tmp = hello('world')
print("-------------------")
print(tmp)

# ===========================================
# Output:
"""
init add_tag with :  p
call add_tag with :  <function hello at 0x7f664cf70268>
-------------------
hello:  <function add_tag.__call__.<locals>.wrap at 0x7f664cf70840>
-------------------
-------------------
<p>hello world</p>
"""
```

## [TOADD] What is it like: both the decorator and to decorated are classes?

```python
# https://www.python.org/dev/peps/pep-0318/#examples
# Example 5:


def provides(*interfaces):
    """
    An actual, working, implementation of provides for
    the current implementation of PyProtocols.  Not
    particularly important for the PEP text.
    """
    def provides(typ):
        declareImplementation(typ, instancesProvide=interfaces)
        return typ
    return provides

class IBar(Interface):
    """Declare something about IBar here"""
    pass

@provides(IBar)
class Foo(object):
    """Implement something here..."""
    pass
```
