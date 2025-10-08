### 1.1: Race Condition

This example demonstrates a **race condition**, one of the most fundamental issues in concurrent programming. Specifically, it shows the "lost update" problem on a shared counter.

A race condition occurs when the correctness of a program depends on the unpredictable timing of concurrent threads or processes.

---

### 🔴 Bad Example (`bad_example.py`)

This script creates multiple threads that all try to increment the same shared counter. Because the increment operation (`value += 1`) is not atomic, threads interfere with each other, and many of the increments are lost.

**To Run:**
```bash
python bad_example.py