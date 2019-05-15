

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
