

# Python notes

Follow note: http://skycrab.github.io/PythonEngineer/.
Summarize and doc here.

## 数据类型, 数据结构

### Make 2 + 2 = 5:

```
>>> import sys
>>> sys.getsizeof(1)      <-- 1, -1, 2 is 28 bytes
28
>>> sys.getsizeof(0)      <-- only 0 is 24 bytes
24
>>> sys.getsizeof(-1)
28
>>> sys.getsizeof(3)
28
>>> id(0)                 <-- all -2, -1, 0, 1, 2 are 32 bytes
140018929931456
>>> id(1)
140018929931488
>>> id(2)
140018929931520
>>> id(-1)
140018929931424
>>> id(-2)
140018929931392
>>>
```
```
>>> import ctypes
# https://docs.python.org/3/library/ctypes.html#ctypes.memmove
>>> ctypes.memmove(id(4), id(5), 28)  
139767155533120
>>> 2 + 2
5
>>> 1 + 2
3
>>> 1 + 3
5
>>> 1 * 4
5
>>> 1 * 5
5
```
```
>>> ctypes.memmove(id(5), id(0), 24)   <-- 24 for 0
140018929931616
>>> 10 / 5
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: division by zero
>>>
```

### 数据结构 - TODO
list, tuple, dict, set

#### lib collections - Container datatypes

 - `namedtuple()`:	factory function for creating tuple subclasses with named fields
 - `deque`:	list-like container with fast appends and pops on either end
 - `OrderedDict`:	dict subclass that remembers the order entries were added
 - `defaultdict`:	dict subclass that calls a factory function to supply missing values


##### collections.namedtuple(typename, field_names, *, rename=False, defaults=None, module=None)


https://docs.python.org/3/library/collections.html

`Returns a new tuple subclass named typename.`

`Named tuple instances do not have per-instance dictionaries`(Joy: defined `__solts__`), so they are `lightweight and require no more memory than regular tuples.`


##### collections.OrderedDict([items])

OrderedDict is implied with a circular doubly linked list.

Big-O running times for all methods are the same as regular dictionaries.


 - Usage: `implementing variants of functools.lru_cache()`
 ```
 class LRU(OrderedDict):
    'Limit size, evicting the least recently looked-up key when full'

    def __init__(self, maxsize=128, *args, **kwds):
        self.maxsize = maxsize
        super().__init__(*args, **kwds)

    def __getitem__(self, key):
        value = super().__getitem__(key)
        self.move_to_end(key)
        return value

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if len(self) > self.maxsize:
            oldest = next(iter(self))
            del self[oldest]
  ```

### TODO: https://docs.python.org/3/library/functools.html#functools.lru_cache

Example of efficiently computing Fibonacci numbers using a cache to implement a dynamic programming technique:



##TODO: read code at https://github.com/python/cpython/blame/3.7/Lib/collections/__init__.py#L316

Test at https://github.com/python/cpython/blob/master/Lib/test/test_collections.py .

```
>>> import collections
>>> Person=collections.namedtuple('Person','name age gender')
>>> p = Person("kh", 2, "f")
>>> p
Person(name='kh', age=2, gender='f')
>>> Person
<class '__main__.Person'>
>>> type(Person)
<class 'type'>
>>> type(p)
<class '__main__.Person'>
>>>
```

#### Queue.Queue



##### collections.namedtuple(typename, field_names, *, rename=False, defaults=None, module=None)


## 推导式与函数式

算法

反射

属性拦截

装饰器

描述符和属性

生成器

元类

垃圾回收

多线程与多进程

其它
