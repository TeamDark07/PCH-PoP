### 2.1: Resource Leaks

A **resource leak** occurs when a program allocates a finite system resource (like a file handle, network socket, or database connection) but fails to release it when it's no longer needed. If this happens repeatedly in a long-running application, it can exhaust all available resources and cause the entire system to crash.

This is a common problem in concurrent programming, where threads can terminate unexpectedly due to unhandled exceptions, skipping the cleanup code.

---

### 🔴 Bad Example (`bad_example.py`)

This script starts a worker thread that opens a file for writing. Before the `file.close()` method can be called, a `ValueError` is raised, causing the thread to terminate immediately. The file handle is never released by the program, resulting in a resource leak. We use a global `set` to track "active resources" to make this leak visible.

**To Run:**
```bash
python bad_example.py