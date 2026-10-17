## go-stuff

My Go workbench: exercises from *The Go Programming Language*, the hands-on side of **CSE 486/586: Distributed Systems** at the **University at Buffalo**, small experiments, and the bigger projects that grow out of them.

## What this is?
This repo is where I work through ideas by actually building them, not just reading slides or book chapters.
Coursework and book exercises live here alongside smaller experiments where I break things on purpose to see why they break, then fix them.

## Layout

| Folder | What goes there |
|---|---|
| [`gopl/`](gopl/) | Exercises from *The Go Programming Language* (Donovan & Kernighan), one folder per exercise |
| [`cse486/`](cse486/) | Distributed systems hands-on from my CSE 486/586 tutorials, one folder per topic |
| [`learning/`](learning/) | Standalone experiments and snippets: concurrency, generics, testing, stdlib deep-dives |
| [`projects/`](projects/) | Bigger, longer-lived work (the distributed filesystem will live here) |

Everything is one Go module (`github.com/MrKat-Merv/go-stuff`), so any program runs from the repo root:

```sh
go run ./gopl/ch01/ex1.1
go test ./cse486/...
go test -race ./...      # before committing anything concurrent
```

### Conventions
- **One program per folder.** Each exercise or demo is its own `package main` (or a package with tests), so `go run` / `go test` just work.
- **Naming:** `gopl/chNN/exN.M/` for book exercises, `cse486/NN-topic/` for course topics, `learning/topic/` for experiments.
- **Deliberately broken versions** stay in the same folder with a `//go:build ignore` line at the top, so they're kept for comparison but don't break the build. Run one with `go run broken_race.go`.
- **Notes:** a short `README.md` in a folder for anything worth remembering: what the exercise asked, what surprised me, what broke.
- Copy `gopl/_template/` or `cse486/_template/` to start something new (folders starting with `_` are ignored by the Go tool).

## Distributed systems topics covered so far

**RPC**: how remote procedure calls work under the hood, and where the abstraction leaks.
**RPC failure semantics**: at-least-once, at-most-once, exactly-once, and why idempotency isn't the whole story.
**MapReduce**: a sequential and distributed implementation, with fault-tolerant task scheduling.
**Concurrency in Go**: goroutines, channels, mutexes, `select`, and the races you get when you skip them.
**Distributed snapshots**: the Chandy-Lamport algorithm, implemented and tested against concurrent, in-flight markers.
**Time in distributed systems**: physical clock synchronization (Cristian's algorithm) and why it isn't enough.
**Logical clocks**: Lamport clocks and vector clocks, and the gap between them (a smaller timestamp is not proof of causality).
...
More will show up here as the course moves into consensus (Raft) and beyond. Progress is tracked in [`cse486/README.md`](cse486/README.md); book progress in [`gopl/README.md`](gopl/README.md).

## Why?

I'm doing this because I want to actually understand distributed systems, not just pass the class.
Most of what's here started as an assignment and then got poked at further, deliberately broken, rerun, compared against real output.
Because that's the only way I've found that the ideas actually stick for me (perhaps I am not really fit for CS).

## Where this is headed?

If this keeps being as interesting as it has been so far, the plan is to:

Take on a **larger personal project**, most likely a **distributed filesystem**, as a way to combine everything from this course into one system that actually has to survive machine failures, network partitions, and concurrent access, not just pass a test suite.
Start contributing to **open-source distributed systems projects** in my free time, once I trust my own understanding enough to be useful rather than a liability.

## Status

Actively growing alongside the course and the book. Code here is written to learn, not to ship: expect scratch files, deliberately broken versions kept around for comparison, and comments explaining **why** something works the way it does, not just what it does.
