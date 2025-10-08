### 6.5: Busy-Waiting / Spinlocks

**Busy-waiting** (or "spinning") is a concurrency anti-pattern where a thread continuously checks for a condition in a tight loop without yielding control of the CPU. This is sometimes called a **spinlock**.

While it might seem like a simple way to wait for something, it is extremely wasteful. A busy-waiting thread will consume **100% of a CPU core**, generating heat, draining battery, and preventing other useful work from being done by other processes on the system. The correct approach is to use a synchronization primitive that allows the thread to sleep until it is notified that the condition has been met.

---

### 🔴 Bad Example (`bad_example.py`)

This script has a "consumer" thread that needs to wait for a "producer" thread to prepare some data. It does this by repeatedly checking a boolean flag in a `while not data_ready: pass` loop.

To measure the waste, we record the total CPU time used by the script.

**To Run:**
```bash
python bad_example.py