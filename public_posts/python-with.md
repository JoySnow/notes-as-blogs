```
Title:   Python-With
Author:  Xiaoxue Wang<xxwjoy@hotmail.com>
Date:    2019-10-21
```

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->
<!-- code_chunk_output -->

- [ with in Python](#with-in-python)
  - [ History](#history)
  - [ With Detail](#with-detail)
    - [ with 语句执行过程](#with-语句执行过程)
    - [ 自定义上下文管理器](#自定义上下文管理器)
      - [ A context_manager Example](#a-context_manager-example)
      - [ Normal case](#normal-case)
      - [ with-body raise error case](#with-body-raise-error-case)
  - [ contextlib](#contextlib)
    - [ @contextmanager](#contextmanager)
  - [ Refers](#refers)

<!-- /code_chunk_output -->


# with in Python


## History

https://docs.python.org/release/2.6/whatsnew/2.6.html#pep-343-the-with-statement

New in py2.5, use as an optional feature, to be enabled by import clause.
In py2.6, always as a keyword.


The `with` statement clarifies code that previously would use try...finally blocks `to ensure that clean-up code is executed`.


## With Detail

Refer to https://www.ibm.com/developerworks/cn/opensource/os-cn-pythonwith/index.html

```python
with context_expression [as target(s)]:
    with-body
```

 - `context_expression`: An expression, return a `context_manager`    
 - `context_manager`: An object with `__enter__` & `__exit__` methods


### with 语句执行过程
```python
# Step-1: Exec context_expression
context_manager = context_expression
exit = type(context_manager).__exit__  
# Step-2: Exec context_manager.__enter__
value = type(context_manager).__enter__(context_manager)
exc = True   # True 表示正常执行，即便有异常也忽略；
             # False 表示重新抛出异常，需要对异常进行处理.
try:
    try:
        target = value  # 如果使用了 as 子句
        # Step-3: Exec with-body
        with-body     # 执行 with-body
    except:
        # Step-4-a: with-body raise error(执行过程中有异常发生),
        #           exec __exit__ with *sys.exc_info().
        exc = False        
        exit_val = exit(context_manager, *sys.exc_info())
        if exit_val:
            # 如果 __exit__ 返回 True，则异常被忽略；
            pass
        else:
            # 如果返回 False(or None)，则重新抛出异常,由外层代码对异常进行处理.
            raise
finally:
    # Step-4-b: with-body 正常退出，
    #          或者通过 statement-body 中的 break/continue/return 语句退出
    #          或者忽略异常退出
    if exc:
        exit(context_manager, None, None, None)
    # 缺省返回 None，None 在布尔上下文中看做是 False
```

### 自定义上下文管理器

- `context_manager.__enter__()`：进入上下文管理器的运行时上下文，在语句体执行前调用。with 语句将该方法的返回值赋值给 as 子句中的 target，如果指定了 as 子句的话.
 - `context_manager.__exit__(exc_type, exc_value, exc_traceback)`: 退出与上下文管理器相关的运行时上下文，返回一个布尔值表示是否对发生的异常进行处理.


#### A context_manager Example
```python
class DummyResource:
    def __init__(self, tag):
        self.tag = tag
        print ('Resource [%s]' % tag)

    def __enter__(self):
        print ('[Enter %s]: Allocate resource.' % self.tag)
        return self                     # 可以返回不同的对象
        # return DummyResource('abc')   # This return value of `__enter__` only affect the
        # return True                   # `as target`'s assignment, the context_expression is  
        # return "abc"                  # still the self.

    def __exit__(self, exc_type, exc_value, exc_tb):
        print('[Exit %s]: Free resource.' % self.tag)
        print('exc_type: <%s>, exc_value: <%s>, exc_tb:<%s> ' % (exc_type, exc_value, exc_tb ))
        if exc_tb is None:
            print( '[Exit %s]: Exited without exception.' % self.tag)
        else:
            print ('[Exit %s]: Exited with exception raised.' % self.tag)
            return False   # 可以省略，缺省的None也是被看做是False
            # return True  # If return True, no raise to outside with.
```

#### Normal case
```python
with DummyResource('Normal') as cm:
    #print("cm.tag: ", cm, cm.tag)
    print( '[with-body] Run without exceptions.')
```


```python
Resource [Normal]
[Enter Normal]: Allocate resource.
Resource [abc]
[with-body] Run without exceptions.
[Exit Normal]: Free resource.
exc_type: <None>, exc_value: <None>, exc_tb:<None>
[Exit Normal]: Exited without exception.
```

#### with-body raise error case

```python
with DummyResource('With-Exception'):
    print( '[with-body] Run with exception.')
    raise Exception("any exception")
    print( '[with-body] Run with exception. Failed to finish statement-body!')
```

```python
Resource [With-Exception]
[Enter With-Exception]: Allocate resource.
Resource [abc]
[with-body] Run with exception.
[Exit With-Exception]: Free resource.
exc_type: <<class 'Exception'>>, exc_value: <any exception>, exc_tb:<<traceback object at 0x7f90c14298c0>>
[Exit With-Exception]: Exited with exception raised.
---------------------------------------------------------------------------
Exception                                 Traceback (most recent call last)
<ipython-input-38-d2dffb5388e9> in <module>
      1 with DummyResource('With-Exception'):
      2     print( '[with-body] Run with exception.')
----> 3     raise Exception("any exception")
      4     print( '[with-body] Run with exception. Failed to finish statement-body!')

Exception: any exception
```

## contextlib

See more detail and examples in doc.
- https://docs.python.org/3/library/contextlib.html
- https://docs.python.org/2/library/contextlib.html

### @contextmanager

```python
from contextlib import contextmanager

@contextmanager
def demo():
    print( '[Allocate resources]')
    print( 'Code before yield-statement executes in __enter__')
    yield( '*** contextmanager demo ***')
    print( 'Code after yield-statement executes in __exit__')
    print( '[Free resources]')

with demo() as value:
    print( 'Assigned Value: %s' % value)
```

```python
[Allocate resources]
Code before yield-statement executes in __enter__
Assigned Value: *** contextmanager demo ***
Code after yield-statement executes in __exit__
[Free resources]
```

## Refers

- https://docs.python.org/release/2.6/whatsnew/2.6.html#pep-343-the-with-statement
- https://www.ibm.com/developerworks/cn/opensource/os-cn-pythonwith/index.html
- https://docs.python.org/3/library/contextlib.html
