package main

import (
    "fmt"
    "time"
    "math/rand"
)


func boring(msg string, c chan string) {
    go func() { // We launch the goroutine from inside the function.
        for i := 0; ; i++ {
            c <- fmt.Sprintf("%s %d", msg, i)
            fmt.Println("generated ", msg, i)
            time.Sleep(time.Duration(rand.Intn(1e3)) * time.Millisecond)
        }
    }()
}

func main() {
    c := make(chan string)  // For sync, like Lock/Mutex
    // c := make(chan string, 3)   // For sync, like Semaphore
    go boring("Ann", c)
    go boring("Joe", c)
    timeout := time.After(3 * time.Second)
    for {
        select {
        case s := <-c:
            fmt.Println(s)
        case <- timeout:
            fmt.Println("You're too slow.")
            return
        }
    }
}
