### 4.5: Start Method Pitfalls (`fork` vs. `spawn`)

Python's `multiprocessing` module can create new processes using different "start methods." The two most common are:

-   **`fork`:** (Default on Linux & macOS) Creates an almost exact copy of the parent process, including its memory. It is very fast.
-   **`spawn`:** (Default on Windows & macOS) Starts a brand new, clean Python interpreter process. It only inherits the necessary resources to run the target function. It is slower but much safer.

The pitfall arises when using `fork` in a **multithreaded program**.

**The Problem (`fork`):** When you `fork` a multithreaded process, the child process gets a copy of the parent's memory, including the state of all locks. However, the child process is single-threaded; it only contains the thread that initiated the fork. If another thread in the parent was holding a lock at the time of the fork, that lock is now **locked forever** in the child, because the thread that would release it doesn't exist. This can cause the child process to deadlock instantly.

---

### 🔴 Bad Example (`bad_example.py`)

This script creates a scenario that is guaranteed to fail on `fork`-based systems.
1.  A background thread is started, which acquires and holds a lock.
2.  The main thread then attempts to create a `multiprocessing.Pool`.
3.  The `Pool` forks a new worker process. This worker inherits the locked lock from the parent.
4.  The program hangs because the worker process's internal mechanisms can deadlock on this inherited, un-releasable lock.

**To Run:**
```bash
python bad_example.py