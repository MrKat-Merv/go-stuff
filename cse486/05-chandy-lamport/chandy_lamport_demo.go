package main

import "fmt"

// Marker is the special token used to trigger the snapshot algorithm.
const Marker = "MARKER"

// Process represents one node in the distributed system.
//
// A process keeps its current tokens, the snapshot it has taken (if any),
// the messages recorded as being in transit on each incoming channel, and a
// record of which channels have already been closed by a marker.
type Process struct {
	name     string
	tokens   map[string]bool
	snapshot map[string]bool // nil until this process has snapshotted
	recording map[string][]string
	closed   map[string]bool
}

// NewProcess builds a process with its initial token set.
func NewProcess(name string, tokens []string) *Process {
	p := &Process{
		name:      name,
		tokens:    map[string]bool{},
		recording: map[string][]string{},
		closed:    map[string]bool{},
	}
	for _, t := range tokens {
		p.tokens[t] = true
	}
	return p
}

// SnapshotNow saves the process's current state if it has not already done so.
// This is the local snapshot step of the Chandy-Lamport algorithm.
func (p *Process) SnapshotNow() {
	if p.snapshot == nil {
		p.snapshot = map[string]bool{}
		for t := range p.tokens {
			p.snapshot[t] = true
		}
		fmt.Printf(" %s snapshots its own state: %s=%v\n", p.name, p.name, keys(p.snapshot))
	}
}

// Receive handles either a normal application message or a snapshot marker.
//
// If the item is a marker, the process may start/finish its local snapshot.
// If the item is a normal token, the process applies it to its state and may
// record it as an in-flight message depending on the snapshot state.
func (p *Process) Receive(channelName, item string, outbound []*Channel) {
	if item == Marker {
		if p.snapshot == nil {
			// First marker: take a snapshot and mark this channel as empty.
			p.SnapshotNow()
			p.closed[channelName] = true
			fmt.Printf(" %s records channel(%s) as EMPTY (first marker)\n", p.name, channelName)
			for _, ch := range outbound {
				fmt.Printf(" %s sends MARKER on outbound %s\n", p.name, ch.name)
				ch.Send(Marker)
			}
		} else {
			// Second marker: the snapshot is complete for this incoming channel.
			recorded := p.recording[channelName]
			p.closed[channelName] = true
			fmt.Printf(" %s FINALIZES channel(%s) = %v (already snapshotted)\n", p.name, channelName, recorded)
		}
	} else {
		// Regular data message: update the process state.
		p.tokens[item] = true // In a real application, the message would normally affect state.
		if p.snapshot != nil && !p.closed[channelName] {
			// If we are already taking a snapshot and this channel is still active,
			// the message is part of the channel's in-flight traffic.
			p.recording[channelName] = append(p.recording[channelName], item)
			fmt.Printf(" %s records token %q as in-flight on channel(%s)\n", p.name, item, channelName)
		}
	}
}

// keys converts a set-like map into a slice so it can be printed clearly.
// The map iteration order is not guaranteed, so the output is best read as a set.
func keys(m map[string]bool) []string {
	var out []string
	for k := range m {
		out = append(out, k)
	}
	return out
}

// Channel models a FIFO communication link between processes.
type Channel struct {
	name  string
	queue []string
}

// Send appends an item to the end of the queue.
func (c *Channel) Send(item string) {
	c.queue = append(c.queue, item)
}

// DeliverNext removes the next item from the channel and delivers it to the destination.
// The outbound parameter tells the destination which channels to notify with markers.
func (c *Channel) DeliverNext(dest *Process, outbound []*Channel) {
	item := c.queue[0]
	c.queue = c.queue[1:]
	dest.Receive(c.name, item, outbound)
}

// main demonstrates a tiny Chandy-Lamport snapshot run between two processes.
func main() {
	p := NewProcess("P", []string{"G"})
	q := NewProcess("Q", []string{"R", "P"})

	// These channels carry data messages between the two processes.
	chPQ := &Channel{name: "P,Q", queue: []string{"Y"}}
	chQP := &Channel{name: "Q,P", queue: []string{"O", "B"}}

	fmt.Println("=== Step 1: P starts a snapshot ===")
	p.SnapshotNow()
	fmt.Println(" P sends MARKER on its outbound channel(P,Q)")
	chPQ.Send(Marker)

	fmt.Println("\n=== Step 2: channel(P,Q) delivers messages to Q in FIFO order ===")
	chPQ.DeliverNext(q, []*Channel{chQP})
	chPQ.DeliverNext(q, []*Channel{chQP})

	fmt.Println("\n=== Step 3: channel(Q,P) delivers messages to P in FIFO order ===")
	chQP.DeliverNext(p, []*Channel{chPQ})
	chQP.DeliverNext(p, []*Channel{chPQ})
	chQP.DeliverNext(p, []*Channel{chPQ})

	fmt.Println("\n=== FINAL GLOBAL SNAPSHOT ===")
	fmt.Printf("  P = %v\n", keys(p.snapshot))
	fmt.Printf("  Q = %v\n", keys(q.snapshot))
	fmt.Printf("  channel(P,Q) = []\n")
	fmt.Printf("  channel(Q,P) = %v\n", p.recording["Q,P"])
}
