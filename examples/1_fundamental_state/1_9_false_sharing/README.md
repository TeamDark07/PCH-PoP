### 1.9: False Sharing

**False sharing** is a subtle hardware-level performance issue, not a correctness bug. It occurs when multiple threads on different CPU cores modify independent variables that happen to reside on the same **CPU cache line**.

A CPU cache line is the smallest unit of memory that a CPU can move from main memory to its local cache (typically 64 bytes). When one thread writes to its variable, the entire cache line is marked as "dirty." This forces other cores using that same cache line to discard their local copy and re-fetch it from a slower memory level, even though their own data wasn't logically changed. This constant invalidation and re-fetching ("cache line ping-pong") can severely degrade performance.

---

### 🔴 Bad Example (`bad_example.py`)

This script creates a list of counters, which places them next to each other in memory. It then spawns multiple threads, each assigned to increment its own independent counter. Because the counters are adjacent, they likely share cache lines, leading to false sharing and poor performance.

**To Run:**
```bash
python bad_example.py