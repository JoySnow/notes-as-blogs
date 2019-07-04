


<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->
<!-- code_chunk_output -->

- [ Implementation of dict in python](#implementation-of-dict-in-python)
  - [ Hash tables](#hash-tables)
    - [ Think how to store the data with hash](#think-how-to-store-the-data-with-hash)
    - [ The goal of a hash function](#the-goal-of-a-hash-function)
    - [ See the example(in blog) of collision, How to workaround?](#see-the-examplein-blog-of-collision-how-to-workaround)
  - [ Open addressing](#open-addressing)
    - [ How python find a free slot?](#how-python-find-a-free-slot)
    - [ Check dictobject.c#L134 for collision-resolution](#check-dictobjectcl134-for-collision-resolution)
  - [ Pre-defined Tips](#pre-defined-tips)
  - [ Dictionary C structures](#dictionary-c-structures)
  - [ Dictionary initialization](#dictionary-initialization)
  - [ Adding/Set items](#addingset-items)
    - [ Call `find_empty_slot` in `insertdict`](#call-find_empty_slot-in-insertdict)
    - [ Call `dk_get_index` in `find_empty_slot`](#call-dk_get_index-in-find_empty_slot)
      - [ DKIX_EMPTY and DKIX_DUMMY](#dkix_empty-and-dkix_dummy)
    - [ Summarize the logic](#summarize-the-logic)
  - [ Removing items](#removing-items)
    - [ Note:](#note)

<!-- /code_chunk_output -->


# Implementation of dict in python

Refer to:
- https://www.laurentluce.com/posts/python-dictionary-implementation/
- https://docs.python.org/3/c-api/dict.html



- http://pybites.blogspot.com/2008/10/pure-python-dictionary-implementation.html

All analysis are based on py3.7's source code:
- https://github.com/python/cpython/blame/3.7/Objects/dictobject.c
- https://docs.python.org/3/c-api/dict.html
- https://docs.python.org/3/library/functions.html
- https://docs.python.org/3/library/stdtypes.html#mapping-types-dict



## Hash tables

> Python dictionaries are implemented using hash tables. It is an array whose indexes are obtained using a hash function on the keys.

### Think how to store the data with hash
- Source: `{key: value}` pairs
- Dest:   claim a C array list, (has a certain length when created.)

```
For each key:
    hash_func(key) => hash => index => list[index]
```

`hash_func` matters.  

### The goal of a hash function
   - To distribute the keys evenly in the array.
   - A good hash function minimizes the number of collisions e.g. different keys having the same hash.

### See the example(in blog) of collision, How to workaround?
 - Use linked list. Increase lookup time(O(1))
 - See how python make this?

## Open addressing

### How python find a free slot?
```c
j = (5*j) + 1 + perturb;
perturb >>= PERTURB_SHIFT;
use j % 2**i as the next table index;
```
- `j` is the `table index`.
- Use current `j` to get a new `j`.

The example of collision:
 - Use linked list. Increase lookup time, ( > O(1) )
 - Python: Open addressing - **use current index to calculate next one**


### Check dictobject.c#L134 for collision-resolution
> In open addressing, when a data item can't be placed at the index calculated by the hash function, another location in the array is sought.
在开放地址法中，若数据不能直接放在由哈希函数计算出来的数组下标所指的单元时，就要寻找数组的其他位置。

```c
perturb >>= PERTURB_SHIFT;
j = (5*j) + 1 + perturb;
use j % 2**i as the next table index;
```
- `j`: index
- `perturb`: a variable
- `PERTURB_SHIFT`: define as 5 in python
- `2**i`: is the current length of list.

Trying to understand ... Refer to https://github.com/python/cpython/blame/3.7/Objects/dictobject.c#L134

1. **First half of collision resolution**: visit table indices via this recurrence:
  `j = ((5*j) + 1) mod 2**i`

	- `2**i` is the current length of list.
	- As the result, probing this `j` `2**i`times, it will visit each value in `range(2**i)`. (like a Linear probing: j += 1.)
	- eg:
		```
		for a table of size 2**3 the order of indices is:
	  	0 -> 1 -> 6 -> 7 -> 4 -> 5 -> 2 -> 3 -> 0 [and here it's repeating]
		```

2. **The other half of the strategy**: To get the other bits of the hash code into play.  
    `j = ((5*j) + 1 + perturb) mod 2**i`
    This is done by initializing a (unsigned) `variable "perturb"` to the full hash code, and changing the recurrence to:   

  ```c
  perturb >>= PERTURB_SHIFT;
  j = (5*j) + 1 + perturb;
  use j % 2**i as the next table index;
  ```

3. `PERTURB_SHIFT = 5` is tested and a good choice as said.


## Pre-defined Tips

- The default size of a new dict is 8.
`#define PyDict_MINSIZE 8`
https://github.com/python/cpython/blob/3.7/Objects/dictobject.c#L104

- To avoid slowing down lookups on a near-full table, we resize the table when it's USABLE_FRACTION (currently two-thirds) full.
`#define USABLE_FRACTION(n) (((n) << 1)/3)`
https://github.com/python/cpython/blob/3.7/Objects/dictobject.c#L104
https://github.com/python/cpython/blob/3.7/Objects/dictobject.c#L374

- Growth rate upon hitting maximum load: `used*3` for py3.7
`#define GROWTH_RATE(d) ((d)->ma_used*3)`  <-- double in size: 2/3 * 3
https://github.com/python/cpython/blob/3.7/Objects/dictobject.c#L400
	```
	/* GROWTH_RATE. Growth rate upon hitting maximum load.
	 * Currently set to used*3.
	 * This means that dicts double in size when growing without deletions,
	 * but have more head room when the number of deletions is on a par with the
	 * number of insertions.  See also bpo-17563 and bpo-33205.
	 *
	 * GROWTH_RATE was set to used*4 up to version 3.2.
	 * GROWTH_RATE was set to used*2 in version 3.3.0
	 * GROWTH_RATE was set to used*2 + capacity/2 in 3.4.0-3.6.0.
	 */
	```

## Dictionary C structures

https://github.com/python/cpython/blob/3.7/Objects/dict-common.h
```c
typedef struct {
    /* Cached hash code of me_key. */
    Py_hash_t me_hash;
    PyObject *me_key;
    PyObject *me_value; /* This field is only meaningful for combined tables */
} PyDictKeyEntry;
```

Doc in https://github.com/python/cpython/blame/3.7/Objects/dictobject.c#L9
Defined in https://github.com/python/cpython/blob/3.7/Objects/dict-common.h#L21

```bash
/* PyDictKeysObject
This implements the dictionary's hashtable.
As of Python 3.6, this is compact and ordered. Basic idea is described here:
* https://mail.python.org/pipermail/python-dev/2012-December/123028.html
* https://morepypy.blogspot.com/2015/01/faster-more-memory-efficient-and-more.html
layout:
+---------------+
| dk_refcnt     |   <-- pyObject reference cnt
| dk_size       |   <-- Size of dk_indices
| dk_lookup     |   <-- Function to lookup in the hash table (dk_indices)
| dk_usable     |   <-- Number of usable entries in dk_entries.
| dk_nentries   |   <-- Number of used entries in dk_entries.
+---------------+
| dk_indices    |   <-- actual a hashtable (list), It holds index of entries,
|               |       list index is converted from hash-value
+---------------+
| dk_entries    |   <-- array of PyDictKeyEntry
|               |
+---------------+
*/
```


## Dictionary initialization
https://github.com/python/cpython/blob/3.7/Objects/dictobject.c#L671
```c
PyObject *
PyDict_New(void)
{
    PyDictKeysObject *keys = new_keys_object(PyDict_MINSIZE);
    if (keys == NULL)
        return NULL;
    return new_dict(keys, NULL);
}
```


## Adding/Set items
https://github.com/python/cpython/blob/3.7/Objects/dictobject.c#L1436
```c
int PyDict_SetItem(PyObject *p, PyObject *key, PyObject *val)
    ...  // make a hash(key)
    /* insertdict() handles any resizing that might be necessary */
    return insertdict(mp, key, hash, value);
```


### Call `find_empty_slot` in `insertdict`
https://github.com/python/cpython/blob/3.7/Objects/dictobject.c#L971
```c
/* Internal function to find slot for an item from its hash
   when it is known that the key is not present in the dict.
   The dict must be combined. */
static Py_ssize_t
find_empty_slot(PyDictKeysObject *keys, Py_hash_t hash)
{
    ...
    const size_t mask = DK_MASK(keys);
    size_t i = hash & mask;                    
    Py_ssize_t ix = dk_get_index(keys, i);     // first try of index
    for (size_t perturb = hash; ix >= 0;) {    //<-- keep *probing* for an
        perturb >>= PERTURB_SHIFT;             //    empty slot, until ix < 0.   
        i = (i*5 + perturb + 1) & mask;        
        ix = dk_get_index(keys, i);
    }
    return i;
}
```


### Call `dk_get_index` in `find_empty_slot`
https://github.com/python/cpython/blob/3.7/Objects/dictobject.c#L313
```c
/* lookup indices.  returns DKIX_EMPTY, DKIX_DUMMY, or ix >=0 */
static inline Py_ssize_t
dk_get_index(PyDictKeysObject *keys, Py_ssize_t i)
```
Return value `ix`:
  - if a valid (DKIX_EMPTY, DKIX_DUMMY), must < 0.
  - once `ix >= 0`, its mean this index has already used.


#### DKIX_EMPTY and DKIX_DUMMY
https://github.com/python/cpython/blob/3.7/Objects/dictobject.c#L45
```c
/*
NOTE: Since negative value is used for DKIX_EMPTY and DKIX_DUMMY, type of
dk_indices entry is signed integer and int16 is used for table which
dk_size == 256.
*/
```
`DKIX_EMPTY` is for empty, and `DKIX_DUMMY` is for used before, but deleted.

### Summarize the logic

```c
hash(key) => hash
hash & mask => i
dk_indices[i] => ix
Once ix >= 0:
   dx_extries[ix] => the target entry
```



## Removing items
https://github.com/python/cpython/blob/3.7/Objects/dictobject.c#L1510
```c
int PyDict_DelItem(PyObject *op, PyObject *key)
{
    Py_hash_t hash;                                  // <-- calculate hash(key)
    ix = (mp->ma_keys->dk_lookup)(mp, key, hash, &old_value);  // get ix with hash
    if (ix >= 0) {
        dk_set_index(mp->ma_keys, hashpos, DKIX_DUMMY);  // fill with DKIX_DUMMY
    }                   // Not really empty this entry, but
    ...
}
```

### Note:
The delete item operation doesn’t trigger an array resize if the number of used slots is much less that the total number of slots.
