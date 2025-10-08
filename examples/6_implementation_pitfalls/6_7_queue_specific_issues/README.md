### 6.7: Queue-Specific Issues

The `queue` module is a cornerstone of thread-safe programming in Python, but it has its own set of common pitfalls that can lead to deadlocks or crashes.

This example focuses on two major issues:
1.  **Improper Shutdown Signaling:** Failing to correctly signal all consumer threads to stop, leaving some of them hanging.
2.  **Unhandled `Empty` Exceptions:** Using non-blocking methods like `get_nowait()` without catching the `queue.Empty` exception, which can crash a worker.

---

### 🔴 Bad Example (`bad_example.py`)

This script demonstrates both problems.
1.  **Shutdown Failure:** The producer sends only one "poison pill" (`None`) to the queue, but there are three consumer threads. The first consumer to get the pill will exit, but the other two will be stuck in a `q.get()` call forever, waiting for work that will never arrive. This causes the program to hang.
2.  **Unhandled Exception Risk:** The consumer starts by calling `q.get_nowait()`. Since the queue is initially empty, this would raise a `queue.Empty` exception. While the example catches it to print a message, in a real application, this unhandled exception would silently terminate the thread.

**To Run:**
```bash
python bad_example.py