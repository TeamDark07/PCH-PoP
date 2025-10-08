### 1.3: Lost Update

A **lost update** occurs when two concurrent threads perform a "read-modify-write" cycle on the same data. If their operations interleave, the update from the first thread to complete its "write" can be overwritten and "lost" by the second thread.

This example uses a shared bank account to demonstrate how concurrent deposits and withdrawals can lead to an incorrect final balance if not properly synchronized.

---

### 🔴 Bad Example (`bad_example.py`)

This script simulates many threads making deposits and withdrawals of the same amount. Since each transaction involves reading the balance, modifying it, and writing it back, there is a window for interference. One thread might read the balance, but before it can write its new value, another thread does the same, leading to one of the transactions being lost.

**To Run:**
```bash
python bad_example.py