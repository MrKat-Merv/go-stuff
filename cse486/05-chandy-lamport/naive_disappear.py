"""
Reproduce the "Problem: Dissappearing tokens" counter-example:
The channels snapshot FIRST (while empty), then messages get sent, then the
processes snapshot afterward -- having already sent those tokens away.
"""

P_tokens = {"G", "Y"}
Q_tokens = {"R", "P", "B", "O"}

print("NAive approach : channels snapshot first, while empty, then messages sent, then processes snapshot afterward")
channel_PQ_snapshot = list()  # channel_PQ snapshots -- empty
channel_QP_snapshot = list()  # channel_QP snapshots -- empty
print(f" channel (P,Q) snapshot taken: {channel_PQ_snapshot}")
print(f" channel (Q,P) snapshot taken: {channel_QP_snapshot}")

print("\nThen, in-flight sends happen after the channels snapshot, but before the processes snapshot")
P_tokens.remove("Y")  # P sends Y to Q
print(" P sends Y (now inflight on channel_PQ, but channel_PQ snapshot was already taken and is empty)")
Q_tokens.remove("B")  # Q sends B to P
Q_tokens.remove("O")  # Q sends O to P
print(" Q sends B and O (now inflight on channel_QP, but channel_QP snapshot was already taken and is empty)")

print("\nNow the processes finally snapshot, after the channels snapshot and after the sends")
P_snapshot = set(P_tokens)    #P snapshots -- no longer holds Y at this instant
Q_snapshot = set(Q_tokens)    #Q snapshots -- no longer holds B or O at this instant
print(f" P snapshot taken: {P_snapshot}")
print(f" Q snapshot taken: {Q_snapshot}")

combined = set(P_snapshot) | set(Q_snapshot) | set(channel_PQ_snapshot) | set(channel_QP_snapshot)
expected_all = {"G", "Y", "R", "P", "B", "O"}
missing = expected_all - combined
print(f"\nCombined snapshot: {sorted(combined)}")
print(f"Missing tokens: {sorted(missing)}")
assert missing == {"Y", "B", "O"}, "Expected missing tokens Y, B, O"
print("\nNaive approach: Dissappearing tokens Y, B, O detected in combined snapshot.")