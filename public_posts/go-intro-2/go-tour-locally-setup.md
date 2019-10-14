

## Play with `Go tour` locally

1. Create a tmp dir and get "tour"
```bash
$ mkdir /tmp/go-tour
$ cd /tmp/go-tour
$ go get golang.org/x/tour
```

2. After the `go get`, `/tmp/go-tour` will still be empty.

```bash
/home/joy/go/src/golang.org/x/tour   <-- `tour` code is put here.
/home/joy/go/bin/tour                <-- go build will be run, and generate bin `tour`.
```

3. Run by command `tour`, can't find it
```bash
$ tour
bash: tour: command not found...
```

4. Add `$HOME/go/bin` to `$PATH`
```bash
$ cat ~/.bash_profile
PATH=$PATH:$HOME/go/bin
$ source ~/.bash_profile
```

5. Now `tour`cmd is good. Any changes in webpage will be stored locally.
```bash
$ tour
2019/09/03 15:02:27 Serving content from /home/joy/go/src/golang.org/x/tour
2019/09/03 15:02:27 A browser window should open. If not, please visit http://127.0.0.1:3999
2019/09/03 15:02:28 accepting connection from: 127.0.0.1:51782
2019/09/03 15:02:42 running snippet from: 127.0.0.1:51782
2019/09/03 15:02:53 running snippet from: 127.0.0.1:51782
2019/09/03 15:03:05 running snippet from: 127.0.0.1:51782
...
```

6. Have fun ... :D
