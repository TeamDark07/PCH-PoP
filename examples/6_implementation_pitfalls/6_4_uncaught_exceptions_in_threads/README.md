### 6.4: Uncaught Exceptions in Threads

A critical and dangerous behavior of Python's `threading.Thread` is that if an exception is raised within the thread's target function and is not caught, it does **not** propagate to the main thread.

The result is that the worker thread will **silently terminate**, and the main program will continue running as if nothing went wrong. This can lead to silent failures, where critical background work fails without any notification, potentially causing data corruption or leaving the application in an inconsistent state.

---

### 🔴 Bad Example (`bad_example.py`)

This script starts a `critical_worker` thread that is designed to fail by raising a `ValueError`. The main thread starts the worker and then continues its own execution. It has no mechanism to know that the worker has crashed.

**To Run:**
```bash
python bad_example.py