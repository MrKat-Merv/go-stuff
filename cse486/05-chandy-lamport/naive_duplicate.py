"""
Reproduce the lecture's "Problem: Duplicated tokens" counter-example":
snapshotting each component independently, with NO marker algorithm at
all, just "everyone snapshots whenever they feel like it."
"""

P_tokens = {"G", "Y"}
Q_tokens = {"R", "P", "B", "O"}
channel_PQ = []
channel_QP = []

print("Naive approch: P snapshots first, THEN sends Y")
P_snapshot = set(P_tokens)    #P snapshots -- still holds Y at this instant
print(f" P snapshot taken: {P_snapshot}")

P_tokens.remove("Y")  
channel_PQ.append("Y")  # P sends Y after snapshotting
channel_PQ.pop(0)
Q_tokens.add("Y")  # Q receives Y
print(f" Y sent and delievered to Q")

Q_tokens = set(Q_tokens)  # Q snapshots -- now holds Y at this instant
print(f" Q snapshot taken: {Q_tokens}")

channel_PQ_snapshot = list(channel_PQ)  # empty, snapshotted last
channel_QP_snapshot = list(channel_QP)  # empty

print(f"\nCombined snapshot: P={P_snapshot}, Q={Q_tokens}, "
      f"channel_PQ={channel_PQ_snapshot}, channel_QP={channel_QP_snapshot}")

combined = list(P_snapshot) + list(Q_tokens) + channel_PQ_snapshot + channel_QP_snapshot
from collections import Counter
counts = Counter(combined)
dupes = {token: count for token, count in counts.items() if count > 1}
print(f"\nDuplicate tokens in combined snapshot: {dupes}")
assert dupes == {"Y": 2}, "Expected duplicate token Y"
print("\nNaive approach: Duplicated token Y detected in combined snapshot.")