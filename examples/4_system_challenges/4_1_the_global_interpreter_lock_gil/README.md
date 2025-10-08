### 4.1: The Global Interpreter Lock (GIL)

The **Global Interpreter Lock (GIL)** is a mutex in the standard CPython interpreter that protects access to Python objects, preventing multiple native threads from executing Python bytecode at the same time within a single process.

**What this means:**
*   **CPU-Bound Tasks:** If your code is performing heavy calculations (e.g., math, data processing), the GIL means that even on a multi-core machine, only one thread can run at a time. Using `threading` for these tasks will **not** result in a performance increase.
*   **I/O-Bound Tasks:** If your code is waiting for external resources (e.g., network requests, disk reads), the GIL is released during these waits. This allows other threads to run, making `threading` highly effective for I/O-bound work.

This example focuses on demonstrating the GIL's impact on a **CPU-bound task**.

---

### 🔴 Bad Example (`bad_example.py`)

This script attempts to speed up a purely computational task (a simple countdown loop) by splitting the work across two threads. It first runs the task twice sequentially to get a baseline time, then runs it with two threads.

**To Run:**
```bash
python bad_example.py