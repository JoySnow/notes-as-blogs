

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->
<!-- code_chunk_output -->

- [ Python Dict Implementation](#python-dict-implementation)
  - [ Pre-Introduction](#pre-introduction)
    - [ Some main data types](#some-main-data-types)
    - [ Used in class : `__dict__`](#used-in-class-__dict__)
    - [ We all know: Dict is using hash for indexing](#we-all-know-dict-is-using-hash-for-indexing)
  - [ Intro of dict 's hash & Related C code](#intro-of-dict-s-hash-related-c-code)
  - [ Demo a Python dict implementation](#demo-a-python-dict-implementation)
  - [ (optional) OrderedDict](#optional-ordereddict)

<!-- /code_chunk_output -->


# Python Dict Implementation

## Pre-Introduction
### Some main data types
https://docs.python.org/3/reference/datamodel.html#the-standard-type-hierarchy

- numbers.Number
- Sequences
  - Immutable sequences
    - Strings
    - Tuples
    - Bytes
  - Mutable sequences
    - Lists
    - Byte Arrays
- Set types
  - Sets
  - Frozen sets
- **Mappings**
  - **Dictionaries**

### Used in class : `__dict__`
- Classes: `__dict__` is the dictionary containing the class’s namespace;
- Class instances: `__dict__` is the attribute dictionary;

```python
In [1]: class C(object):
   ...:     x = 4
   ...:  
   ...: c = C()
   ...: c.y = 5
   ...: c.__dict__, type(c.__dict__)                                                                                                                                         
Out[1]: ({'y': 5}, dict)

In [2]: C.__dict__, type(C.__dict__)                                                                                                                                         
Out[2]:
(mappingproxy({'__module__': '__main__',
               'x': 4,
               '__dict__': <attribute '__dict__' of 'C' objects>,
               '__weakref__': <attribute '__weakref__' of 'C' objects>,
               '__doc__': None}),
 mappingproxy)

In [4]: import collections                                                              

In [5]: isinstance(C.__dict__  , collections.Mapping)                                                            
Out[5]: True

In [6]: type(type.__dict__)                                                             
Out[6]: mappingproxy
```

### We all know: Dict is using hash for indexing


## Intro of dict 's hash & Related C code

Follow:
- `./python-dict-implementaion.md`
- https://www.laurentluce.com/posts/python-dictionary-implementation/

## Demo a Python dict implementation
See `./python-dict-implementation.ipynb`

## (optional) OrderedDict
