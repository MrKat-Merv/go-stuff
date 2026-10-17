# The Go Programming Language — exercises

Solutions to exercises from *The Go Programming Language* by Alan A. A. Donovan and Brian W. Kernighan.

## Layout

```
gopl/
├── ch01/
│   ├── ex1.1/main.go
│   ├── ex1.2/main.go
│   └── ...
├── ch02/
└── ...
```

Each exercise is its own folder named after the book's numbering, so it runs on its own:

```sh
go run ./gopl/ch01/ex1.1 arg1 arg2
go test ./gopl/ch02/ex2.2
```

To start a new one: `cp -r gopl/_template gopl/ch01/ex1.3`, then fill in the header comment with the exercise prompt in your own words.

When an exercise builds on the book's example program (echo, dup, lissajous, fetch...), copy the example into the exercise folder and modify it there, so each folder stands on its own.

## Progress

| Ch | Topic | Status | Notes |
|---|---|---|---|
| 1 | Tutorial | ⬜ | |
| 2 | Program Structure | ⬜ | |
| 3 | Basic Data Types | ⬜ | |
| 4 | Composite Types | ⬜ | |
| 5 | Functions | ⬜ | |
| 6 | Methods | ⬜ | |
| 7 | Interfaces | ⬜ | |
| 8 | Goroutines and Channels | ⬜ | |
| 9 | Concurrency with Shared Variables | ⬜ | |
| 10 | Packages and the Go Tool | ⬜ | |
| 11 | Testing | ⬜ | |
| 12 | Reflection | ⬜ | |
| 13 | Low-Level Programming | ⬜ | |

⬜ not started · 🟨 in progress · ✅ done

Chapters 8 and 9 overlap heavily with the concurrency work in [`../cse486`](../cse486); worth cross-linking when they get done.
