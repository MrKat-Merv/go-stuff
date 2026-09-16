## go-stuff

Go code and notes from learning distributed systems.  
Written while taking **CSE 486/586: Distributed Systems** at the **University at Buffalo**, plus personal experiments on the side.  

## What this is?  
This repo is where I work through the ideas from class by actually building them, not just reading slides.   
Coursework lives here alongside smaller experiments where I break things on purpose to see why they break, then fix them.  

Topics covered so far:  

**RPC**: how remote procedure calls work under the hood, and where the abstraction leaks.  
**RPC failure semantics**: at-least-once, at-most-once, exactly-once, and why idempotency isn't the whole story.  
**MapReduce**: a sequential and distributed implementation, with fault-tolerant task scheduling.  
**Concurrency in Go**: goroutines, channels, mutexes, `select`, and the races you get when you skip them.  
**Distributed snapshots**: the Chandy-Lamport algorithm, implemented and tested against concurrent, in-flight markers.  
**Time in distributed systems**: physical clock synchronization (Cristian's algorithm) and why it isn't enough.  
**Logical clocks**: Lamport clocks and vector clocks, and the gap between them (a smaller timestamp is not proof of causality).  
...  
More will show up here as the course moves into consensus (Raft) and beyond.  

## Why?  

I'm doing this because I want to actually understand distributed systems, not just pass the class.   
Most of what's here started as an assignment and then got poked at further, deliberately broken, rerun, compared against real output.   
Because that's the only way I've found that the ideas actually stick for me (perhaps I am not really fit for CS).  

## Where this is headed?  

If this keeps being as interesting as it has been so far, the plan is to:  

Take on a **larger personal project**, most likely a **distributed filesystem**, as a way to combine everything from this course into one system that actually has to survive machine failures, network partitions, and concurrent access, not just pass a test suite.  
Start contributing to **open-source distributed systems projects** in my free time, once I trust my own understanding enough to be useful rather than a liability.  

## Status:  

Actively growing alongside the course. Code here is written to learn, not to ship, expect scratch files, deliberately broken versions kept around for comparison, and comments explaining **why** something works the way it does, not just what it does.  
