```
Title:   An-Intro-of-Go
Author:  Xiaoxue Wang<xxwjoy@hotmail.com>
Date:    2019-10-14
```

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->
<!-- code_chunk_output -->

- [ An Intro of Go](#an-intro-of-go)
  - [ Go's Design, History, ...](#gos-design-history)
    - [ Go start time](#go-start-time)
    - [ Why a new language is needed?](#why-a-new-language-is-needed)
    - [ Here comes the go ...](#here-comes-the-go)
    - [ some guiding design principles](#some-guiding-design-principles)
    - [ Usage](#usage)
      - [ Is Google using Go internally?](#is-google-using-go-internally)
      - [ What other companies use Go?](#what-other-companies-use-go)
  - [ Go's basic grammar](#gos-basic-grammar)
    - [ tips](#tips)
  - [ Go concurrency](#go-concurrency)
    - [ What is concurrency?](#what-is-concurrency)
    - [ Go supports concurrency by providing ...](#go-supports-concurrency-by-providing)
    - [ Examples](#examples)
  - [ References](#references)

<!-- /code_chunk_output -->


# An Intro of Go

https://golang.org/doc/



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


## Go's basic grammar

Online:
 - https://tour.golang.org/   
 - https://tour.go-zh.org/

Local: http://127.0.0.1:3999/welcome/1    
Refer to ./go-tour-locally-setup.md .    

### tips

- package
- import
- func
- for loop
- goroutine
- channel
- select


## Go concurrency

A main feature in Go.

### What is concurrency?
Concurrency is the composition of independently executing computations.

Concurrency is a way to structure software, particularly as a way to write clean code that interacts well with the real world.

It is not parallelism.

(JOY: Concurrency is a way to structure software, break the processing down.
      You can have many solutions(concurrent design) to solve a problem.
      If a concurrent design can be parallelizable, then it's also parallelism. )

Refer to https://talks.golang.org/2012/concurrency.slide#6 & 7 .      

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


## References

 - https://golang.org
 - https://golang.google.cn/doc/faq
 - Slide [Go Concurrency Patterns: by Rob Pike](https://talks.golang.org/2012/concurrency.slide#1)
 - Slide [Concurrency is not Parallelism: by Rob Pike](https://talks.golang.org/2012/waza.slide#1)
