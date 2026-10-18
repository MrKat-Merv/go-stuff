"""
A runnable simulation of the Chandy-Lamport distributed snapshot algorithm.

This is a beginner-friendly example of how a distributed system can record a
consistent global snapshot without stopping the whole system.

The idea is:
- Each process records its own local state.
- When a special MARKER message is received, the process records the messages
  that were in transit on that channel.
- The algorithm works even when messages are still moving around.

In this demo, we simulate two processes, P and Q, and the channels between them.
"""

# A special control message used to trigger snapshot recording.
MARKER = "MARKER"


class Process:
    """Represents one node in the distributed system."""

    def __init__(self, name, tokens):
        # Human-readable process name, like "P" or "Q".
        self.name = name

        # The process's current local data/items.
        # We store it in a set so each token is unique.
        self.tokens = set(tokens)

        # snapshot is the copy of the process state taken during the algorithm.
        # It starts as None until the process records its first snapshot.
        self.snapshot = None

        # recording stores messages that were in flight on each incoming channel.
        # Example: {'Q,P': ['O', 'B']} means messages seen in transit from Q to P.
        self.recording = {}

        # closed keeps track of channels for which the snapshot is already finalized.
        self.closed = set()

    def snapshot_now(self):
        """Save a local snapshot of this process if one has not been taken yet."""
        if self.snapshot is None:
            # Copy the current token set so we can compare later.
            self.snapshot = set(self.tokens)
            print(f" {self.name} snapshot its own state: {self.name}={self.snapshot}")

    def receive(self, inbound_channel_name, item, outbound_channels):
        """
        Handle a message coming into this process.

        inbound_channel_name: which channel the message arrived on.
        item: the actual payload or control marker.
        outbound_channels: the channels this process can send on next.
        """
        if item == MARKER:
            # This is a control message used by Chandy-Lamport to trigger a snapshot.
            if self.snapshot is None:
                # First time this process sees a marker: it must record its state.
                self.snapshot_now()

                # No messages before this marker are considered in-flight on this channel.
                self.closed.add(inbound_channel_name)

                # Send the marker to all outgoing channels to continue the snapshot wave.
                for ch in outbound_channels:
                    print(f" {self.name} sends MARKER on outbound {ch.name}")
                    ch.send(MARKER)
            else:
                # The process already recorded its state. This marker means the
                # current channel's in-flight messages are complete.
                recorded = self.recording.get(inbound_channel_name, [])
                self.closed.add(inbound_channel_name)
                print(
                    f" {self.name} FINALIZES channel({inbound_channel_name}) = "
                    f"{recorded} (already snapshotted)"
                )
        else:
            # Regular application data: the process processes it as normal.
            self.tokens.add(item)

            # If a snapshot has started and this channel is still active, record
            # the message as being in transit on that channel.
            if self.snapshot is not None and inbound_channel_name not in self.closed:
                self.recording.setdefault(inbound_channel_name, []).append(item)
                print(
                    f" {self.name} records token {item!r} as in-flight on "
                    f"channel({inbound_channel_name})"
                )


class Channel:
    """A FIFO queue representing a communication channel between processes."""

    def __init__(self, name):
        self.name = name
        self.queue = []

    def send(self, item):
        """Put an item at the end of the channel."""
        self.queue.append(item)

    def deliver_next(self, dest_process, outbound_channels_of_dest):
        """
        Deliver the next message from this channel to the destination process.

        This is a simple simulation of network delivery in order.
        """
        item = self.queue.pop(0)
        dest_process.receive(self.name, item, outbound_channels_of_dest)


# --- Set up the exact starting state from the slides ---
# P starts with token G, Q starts with tokens R and P.
P = Process("P", tokens={"G"})
Q = Process("Q", tokens={"R", "P"})

# Two channels: P -> Q and Q -> P
ch_PQ = Channel("P,Q")
ch_QP = Channel("Q,P")

# These messages are already on the network before the snapshot starts.
# They have been sent but not yet received.
ch_PQ.queue = ["Y"]  # P sent Y to Q, but Q has not received it yet
ch_QP.queue = ["O", "B"]  # Q sent O and B to P, but P has not received them yet

print("\n=== Step 1: drop the marker at P ===")
# The snapshot starts at P.
P.snapshot_now()
print("  P sends MARKER on channel(P,Q)")
# Add a marker after the already-sent Y, so Q will see Y then the marker.
ch_PQ.queue.append(MARKER)

print("\n=== Step 2: channel (P,Q) delivers to Q, in FIFO order ===")
# FIFO delivery means messages are processed in the order they were sent.
ch_PQ.deliver_next(Q, outbound_channels_of_dest=[ch_QP])  # delivers Y
ch_PQ.deliver_next(Q, outbound_channels_of_dest=[ch_QP])  # delivers MARKER

print("\n=== Step 3: channel (Q,P) delivers to P, in FIFO order ===")
ch_QP.deliver_next(P, outbound_channels_of_dest=[ch_PQ])  # delivers O
ch_QP.deliver_next(P, outbound_channels_of_dest=[ch_PQ])  # delivers B
ch_QP.deliver_next(P, outbound_channels_of_dest=[ch_PQ])  # delivers MARKER

print("\n=== FINAL GLOBAL SNAPSHOT ===")
print(f" P = {P.snapshot}")
print(f" Q = {Q.snapshot}")
print(f" channel(P,Q) = []")
print(f" channel(Q,P) = {P.recording.get('Q,P', [])}")

# Combine the local snapshots and recorded in-flight messages.
all_tokens = set(P.snapshot) | set(Q.snapshot) | set(P.recording.get('Q,P', []))
expected = {"G", "R", "P", "Y", "O", "B"}

# If the algorithm is correct, this set should match the expected tokens.
assert all_tokens == expected, f"MISMATCH! got {all_tokens}, but got {expected}"
print("\nChandy-Lamport algorithm: No duplicate tokens detected in combined snapshot.")
