### 6.6: Misuse of `concurrent.futures`

The `concurrent.futures` module provides a high-level and easy-to-use interface for running tasks concurrently. It offers two main types of executors:
-   **`ThreadPoolExecutor`:** Uses a pool of threads.
-   **`ProcessPoolExecutor`:** Uses a pool of processes.

A common pitfall is choosing the wrong executor for the type of workload, which can lead to code that is significantly slower than a simple, sequential implementation. This mistake stems from not understanding the fundamental trade-offs between threads and processes in Python.

The rule of thumb is simple and critical:
-   **Use `ThreadPoolExecutor` for I/O-bound tasks.**
-   **Use `ProcessPoolExecutor` for CPU-bound tasks.**

---

### 🔴 Bad Example (`bad_example.py`)

This script demonstrates two incorrect choices:

1.  **Using `ThreadPoolExecutor` for a CPU-bound task:** It tries to run a heavy calculation with two threads. Because of the Global Interpreter Lock (GIL), the threads cannot run in parallel, and the total time is the sum of the individual task times (no speedup).
2.  **Using `ProcessPoolExecutor` for an I/O-bound task:** It runs 10 quick I/O operations. The high overhead of creating processes and serializing data makes this approach much slower than using lightweight threads.

**To Run:**
```bash
python bad_example.py