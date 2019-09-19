```
Title:   An-Intro-of-Go
Author:  Xiaoxue Wang<xxwjoy@hotmail.com>
Date:    2019-09-05
```

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->
<!-- code_chunk_output -->

- [ An Intro of Go](#an-intro-of-go)
  - [ * Learning Go's basic grammar](#learning-gos-basic-grammar)
  - [ Go's Design, History, ...](#gos-design-history)
    - [ Go start time](#go-start-time)
    - [ Why a new language is needed?](#why-a-new-language-is-needed)
    - [ Here comes the go ...](#here-comes-the-go)
    - [ some guiding design principles](#some-guiding-design-principles)
    - [ Usage](#usage)
      - [ Is Google using Go internally?](#is-google-using-go-internally)
      - [ What other companies use Go?](#what-other-companies-use-go)
    - [ * Design](#design)
      - [ Build concurrency on the ideas of CSP](#build-concurrency-on-the-ideas-of-csp)
      - [ Why goroutines instead of threads?](#why-goroutines-instead-of-threads)
  - [ Go concurrency examples](#go-concurrency-examples)
    - [ * What is concurrency?](#what-is-concurrency)
    - [ Go supports concurrency by providing ...](#go-supports-concurrency-by-providing)
    - [ Examples](#examples)
  - [ Python consumer & producer examples](#python-consumer-producer-examples)
  - [ References](#references)

<!-- /code_chunk_output -->


# An Intro of Go

https://golang.org/doc/


## * Learning Go's basic grammar

Online: https://tour.golang.org/   
Local: http://127.0.0.1:3999/welcome/1    
Refer to ./go-tour-locally-setup.md .    


## Go's Design, History, ...

See from FAQ: https://golang.google.cn/doc/faq

### Go start time

Go sketch: September 21, 2007.   
Go open source: November 10, 2009.   

### Why a new language is needed?

- frustrated with the language to develop server software
  - choose ease over safety and efficiency: (not all available in one language)
     - efficiency and safety of a statically typed, compiled language
        - C++
        - Java
     - ease of programming of an interpreted, dynamically typed language
        - Python
        - JavaScript
- Computers are quicker, yet not the programming.
- Multiprocessors are universal, yet languages can not support well.

### Here comes the go ...
Go aims to meet all the above advantages/requirements.
A **statically and strong typed, compiled language**.

To meet these goals required addressing a number of linguistic issues:
 - an expressive but lightweight type system;
 - concurrency and garbage collection;
 - rigid dependency specification;
 - and so on.

These cannot be addressed well by libraries or tools; a new language was called for.


More to know: [Go at Google: Language Design in the Service of Software Engineering](https://talks.golang.org/2012/splash.article)


### some guiding design principles

The important principles:
 - no type hierarchy
 - keep the concepts orthogonal:
    - Methods can be implemented for any type;
    - structures represent data;
    - interfaces represent abstraction;
    - and so on.

### Usage

#### Is Google using Go internally?

Go is used widely in production inside Google:
 - golang.org
 - dl.google.com (Google's download server)

A key language for a number of areas:
  - site reliability engineering (SRE)
  - large-scale data processing

#### What other companies use Go?
 - Docker
 - Kubernetes


### * Design

#### Build concurrency on the ideas of CSP

high-level linguistic support for concurrency comes from Hoare's Communicating Sequential Processes, or CSP.
Occam and Erlang are two well known languages that stem from CSP.

#### Why goroutines instead of threads?
Goroutines are part of making concurrency easy to use. The idea, which has been around for a while, is to multiplex independently executing functions—coroutines—onto a set of threads.

**When a coroutine blocks, such as by calling a blocking system call, the run-time automatically moves other coroutines on the same operating system thread to a different, runnable thread so they won't be blocked.** The programmer sees none of this, which is the point.

The result, which we call goroutines, can be very cheap: they have little overhead beyond the memory for the stack, which is just a few kilobytes.
To make the stacks small, Go's run-time uses resizable, bounded stacks.
A newly minted goroutine is given a few kilobytes, which is almost always enough. When it isn't, the run-time grows (and shrinks) the memory for storing the stack automatically, allowing many goroutines to live in a modest amount of memory. The CPU overhead averages about three cheap instructions per function call. It is practical to create hundreds of thousands of goroutines in the same address space. If goroutines were just threads, system resources would run out at a much smaller number.


## Go concurrency examples

### * What is concurrency?
Concurrency is the composition of independently executing computations.

Concurrency is a way to structure software, particularly as a way to write clean code that interacts well with the real world.

It is not parallelism.

(JOY: Concurrency is a way to structure software, break the processing down.
      You can have many solutions(concurrent design) to solve a problem.
      If a concurrent design can is parallelizable, then it's also parallelism. )

Refer to https://talks.golang.org/2012/concurrency.slide#6 .      

### Go supports concurrency by providing ...
 - concurrent execution (`goroutines`)
 - synchronization and messaging (`channels`)
 - multi-way concurrent control (`select`)

Refer to https://talks.golang.org/2012/waza.slide#4 .

### Examples

See examples in
https://talks.golang.org/2012/concurrency.slide#12
to
https://talks.golang.org/2012/concurrency.slide#36

- normal
- goroutine
- communicate via channel
- control via select


## Python consumer & producer examples

Example in ./asyncio-comsumer-producer-queue.py


## References

 - https://golang.org
 - https://golang.google.cn/doc/faq
 - Slide [Go Concurrency Patterns: by Rob Pike](https://talks.golang.org/2012/concurrency.slide#1)
 - Slide [Concurrency is not Parallelism: by Rob Pike](https://talks.golang.org/2012/waza.slide#1)
