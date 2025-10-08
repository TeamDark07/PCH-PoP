### 4.2: Process vs. Thread Choice

Choosing the correct concurrency model,threading or multiprocessing,is one of the most critical architectural decisions you can make in Python. Making the wrong choice can lead to code that is slower than a simple sequential version.

The decision depends entirely on the nature of your workload:
-   **I/O-Bound Work:** The task spends most of its time waiting for external resources (e.g., network, disk, database). The limiting factor is not the CPU.
-   **CPU-Bound Work:** The task spends most of its time performing computations. The limiting factor is the CPU's speed.

The rule of thumb is:
-   **Use `threading` for I/O-bound tasks.** Threads are lightweight and efficiently handle waiting.
-   **Use `multiprocessing` for CPU-bound tasks.** Processes bypass the GIL and can run in true parallel.

---

### 🔴 Bad Example (`bad_example.py`)

This script demonstrates two common mistakes:
1.  **Using `ProcessPoolExecutor` for an I/O-bound task.** It makes 20 quick network requests. The overhead of creating new processes and serializing (pickling) the task data is significant and makes this approach slow.
2.  **Using `ThreadPoolExecutor` for a CPU-bound task.** It runs 4 heavy calculations. The Global Interpreter Lock (GIL) prevents the threads from running in parallel, resulting in no performance gain.

**To Run:**
```bash
python bad_example.py