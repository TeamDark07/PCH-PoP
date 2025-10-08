### 1.7: Memory Visibility Issues

A **memory visibility issue** occurs when a change to a shared variable made by one thread is not seen by other threads. This is because modern multi-core CPUs each have their own local caches. A write operation by one thread might only update its local cache, and the change isn't immediately flushed to main memory, making it "invisible" to threads running on other cores.

---

### A Note on CPython

Reproducing this issue reliably in standard Python (CPython) is very difficult. The Global Interpreter Lock (GIL) often acts as an implicit memory synchronizer during thread context switches, which can hide the problem.

However, this pattern is **extremely dangerous** and can fail in:
*   Other Python implementations (Jython, IronPython).
*   Python code using C extensions that release the GIL (like NumPy).
*   Certain CPU architectures with "weaker" memory models.

The `bad_example.py` demonstrates the dangerous pattern, even if it doesn't always fail in CPython.

---

### 🔴 Bad Example (`bad_example.py`)

This script uses a simple global boolean flag (`done = False`) to signal a worker thread to stop its busy-wait loop. The worker thread spins continuously, checking the flag's value. This pattern is unsafe because the worker thread might be reading a stale, cached value of `done` and never see the `True` value written by the main thread, causing it to hang indefinitely.

**To Run:**
```bash
python bad_example.py