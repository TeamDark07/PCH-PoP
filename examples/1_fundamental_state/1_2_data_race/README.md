### 1.2: Data Race

A **data race** is a specific type of race condition that occurs when multiple threads access the same memory location concurrently, at least one access is a write, and there is no synchronization. This can lead to unpredictable behavior and data corruption.

This example demonstrates a data race on a shared list, where multiple threads corrupt the list's contents by modifying its elements without locks.

---

### 🔴 Bad Example (`bad_example.py`)

This script spawns several threads, each of which iterates over a shared list of zeros and adds its own thread ID to each element. Because there is no locking, threads overwrite each other's work, resulting in a corrupted final list where the values are incorrect.

**To Run:**
```bash
python bad_example.py