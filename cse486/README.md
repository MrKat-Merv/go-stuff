# CSE 486/586 — Distributed Systems hands-on

Code from my own tutorials for CSE 486/586 at the University at Buffalo: each topic gets built, tested, deliberately broken, and fixed.

## Layout

One numbered folder per topic, in the order the course covers them. Inside a topic, split into subpackages when it grows (e.g. `coordinator/`, `worker/`, `cmd/`).

```
cse486/
├── 01-rpc/
│   ├── README.md          # what the tutorial covers, what to try, what broke
│   ├── server/
│   ├── client/
│   └── rpc_test.go
├── 02-rpc-failure-semantics/
└── ...
```

To start a topic: `cp -r cse486/_template cse486/NN-topic`.

Run tests with the race detector; most bugs in this course are races:

```sh
go test -race ./cse486/...
```

## Topics

| # | Folder | Topic | Status |
|---|---|---|---|
| 01 | `01-rpc` | RPC internals and where the abstraction leaks | ⬜ |
| 02 | `02-rpc-failure-semantics` | At-least-once, at-most-once, exactly-once, idempotency | ⬜ |
| 03 | `03-mapreduce` | Sequential + distributed MapReduce, fault-tolerant scheduling | ⬜ |
| 04 | `04-concurrency` | Goroutines, channels, mutexes, `select`, races | ⬜ |
| 05 | `05-chandy-lamport` | Distributed snapshots with in-flight markers | ⬜ |
| 06 | `06-clock-sync` | Physical clock sync, Cristian's algorithm | ⬜ |
| 07 | `07-logical-clocks` | Lamport and vector clocks | ⬜ |
| 08 | `08-raft` | Consensus | ⬜ |

⬜ code not in repo yet · 🟨 in progress · ✅ done
