```
Title:   Python-build-in-any
Author:  Xiaoxue Wang<xxwjoy@hotmail.com>
Date:    2019-10-17
```

# Python's builtin function `any`


## Question about `any`
About `any`, I am not sure if it will break directly when finding a True.   
Even though [the offical doc](https://docs.python.org/3/library/functions.html#any) say so, I still suspect this.    

As said, `any` equivalent to:
```python
def any(iterable):
    for element in iterable:
        if element:
            return True
    return False
```

## Do my own test

I made `foo` and `bar` to test the running time.    
If `any` do `break`, it won't need to iterate through the whole list of `to_check`.    
It can return at second try.    

```
In [6]: to_check = list(range(10000))     <-- do some changes to to_check[:3]

In [10]: to_check[:3]
Out[10]: [1, 0, 2]

In [16]: def foo(src=to_check):           <-- call any
    ...:     return any([not v for v in src])
    ...:

In [17]: def bar(src=to_check):           <-- do my own break
    ...:     for v in src:
    ...:         if not v:
    ...:             return True
    ...:     return False
    ...:

In [24]: timeit.timeit( bar, number=10000)
Out[24]: 0.001488261972554028

In [25]: timeit.timeit( foo, number=10000)
Out[25]: 2.4102902989834547
```

The outcome is in my side, that the `any` doesn't do the `break`.   
So, not same as [the offical doc](https://docs.python.org/3/library/functions.html#any) says.   
Something wrong.  
We better to check for the source code to see why not use `break`. (Python should.)

## Source code
With the help of [an answer in stackoverflow](https://stackoverflow.com/a/27213831/7398389),
I finally get the [source code](https://github.com/python/cpython/blob/3.8/Python/bltinmodule.c#L378).      
The C code shows that it uses break. (Of course, python use the better way.)

So, the issue is in my testcases.


## Do my test AGAIN
`builtin_any` accept an iterable Object, and do the logic just like:
```python
def any(iterable):
    for element in iterable:
        if element:
            return True
    return False
```

Am I feeding way for `any` wrong?
I give it a list. **OH**, the list needs to be generated first. That's the time eater.
```
In [16]: def foo(src=to_check):                   <-- call any
    ...:     return any([not v for v in src])
    ...:
```

GREAT! So I change the feeding to `any` like this, then it work out good. :D
```
In [30]: def foo1(src=to_check):
    ...:     return any(not v for v in src)
    ...:


In [33]: timeit.timeit( foo1, number=10000)       <-- very need to `bar`
Out[33]: 0.0050231619970873

In [34]: timeit.timeit( bar, number=10000)
Out[34]: 0.003690616926178336

In [35]: timeit.timeit( foo, number=10000)
Out[35]: 2.4375523609342054
```

## Summary
`any` do `break`. But pay attention to the feeding.


## Refer to
- https://docs.python.org/3/library/functions.html#any
- https://stackoverflow.com/a/27213831/7398389),
- https://github.com/python/cpython/blob/3.8/Python/bltinmodule.c#L378
