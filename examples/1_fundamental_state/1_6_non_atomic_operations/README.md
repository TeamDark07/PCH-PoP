### 1.6: Non-Atomic Operations

An **atomic operation** is one that is indivisible,it either completes fully or not at all, and it cannot be interrupted midway. In concurrency, it's a common mistake to assume that a single line of code is atomic.

This example proves that a simple operation like `x += 1` is **not atomic** in Python. It is actually a sequence of "read-modify-write" steps. A thread can be paused by the OS after reading the value but before writing the new one, leading to race conditions.

---

### 🔴 Bad Example (`bad_example.py`)

This script first uses Python's built-in `dis` (disassembler) module to show the multiple bytecode instructions that make up the `+=` operation. Then, it runs a simulation where multiple threads perform this non-atomic increment on a shared counter, leading to an incorrect final result.

**To Run:**
```bash
python bad_example.py