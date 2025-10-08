### 2.4: Daemon Thread Pitfalls

A **daemon thread** is a background thread that does not prevent the main program from exiting. When a Python program exits, it checks if any non-daemon threads are still running. If there are, it waits for them. If only daemon threads are left, the interpreter shuts down immediately, **abruptly terminating all daemon threads**.

This behavior is dangerous for any task that needs to perform cleanup, save state, or release resources. Using a daemon thread for a critical task can lead to data corruption or resource leaks.

---

### 🔴 Bad Example (`bad_example.py`)

This script starts a logger as a `daemon=True` thread. Its job is to write log entries and a final "SHUTDOWN CLEANLY" message to a file. The main thread only runs for a short time and then exits. Because the logger is a daemon, it is killed mid-operation.

**To Run:**
```bash
python bad_example.py