```
Title:   Concurrency-and-Parallelism
vagrant-note
Author:  Xiaoxue Wang<xxwjoy@hotmail.com>
Date:    2019-05-08
```


# 并发（concurrency）和并行（parallelism）



## 并行 parallelism

Multi-cpu, so each cpu can handle one task at same time.


## 并发 concurrency

Single-cpu, it will slice the cpu time for multi-tasks.


## GIL (global interpreter lock) (全局解释器)

每个**线程**在执行时候都需要先获取GIL，保证同一时刻只有一个线程可以执行代码，
`即同一时刻只有一个线程使用CPU`，也就是说多线程并不是真正意义上的同时执行.
TODO

## Refer to
https://blog.csdn.net/just_tigris/article/details/87030799
https://blog.csdn.net/weixin_41594007/article/details/79485847
