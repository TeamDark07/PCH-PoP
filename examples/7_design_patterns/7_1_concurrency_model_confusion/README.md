### 7.1: Concurrency Model Confusion

A fundamental design error in Python concurrency is confusing the memory models of `threading` and `multiprocessing` and trying to use their tools interchangeably.

-   **`threading` uses a Shared Memory model.** All threads within a single process operate on the same memory space. They can directly modify the same objects. Primitives like `threading.Lock` work because all threads can see and interact with the same lock object.

-   **`multiprocessing` uses a Separate Memory model.** Each process is a completely separate program with its own memory space. They cannot directly access each other's objects. A variable in one process is just a copy and is invisible to others.

This means you **cannot** use `threading` primitives (like `threading.Lock`) to synchronize `multiprocessing` processes.

---

### 🔴 Bad Example (`bad_example.py`)

This script attempts to use multiprocessing to update a shared dictionary. However, it makes two critical mistakes:
1.  It uses a regular Python dictionary (`shared_cache = {}`) and expects child processes to modify it.
2.  It uses a `threading.Lock` to try and protect access to this dictionary.

This fails completely. Each child process gets its own independent copy of the dictionary and the lock. The modifications are made to these local copies and are lost forever when the process exits. The lock provides no actual synchronization between the processes.

**To Run:**
```bash
python bad_example.py