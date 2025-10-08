### 6.2: Blocking in Critical Sections

A **critical section** is a block of code that must be executed atomically, typically protected by a lock. A major performance anti-pattern is to perform slow, blocking operations,like network I/O, disk access, or long computations,while holding a lock.

When a thread holds a lock, it prevents all other threads from entering that critical section. If the holding thread is busy waiting for a slow operation, it unnecessarily stalls other threads that might only need quick access to the resource, severely reducing the application's overall concurrency and responsiveness.

**The Golden Rule:** Keep your critical sections as short and as fast as possible.

---

### 🔴 Bad Example (`bad_example.py`)

This script simulates fetching data from a slow API to populate a shared cache.
1.  Thread-A acquires a lock to protect the cache.
2.  It discovers a cache miss and proceeds to make a 2-second network request **while still holding the lock**.
3.  During these 2 seconds, Thread-B starts and tries to check the cache. It is immediately blocked, waiting for Thread-A.
4.  Only after Thread-A's slow network call completes and it releases the lock can Thread-B finally run.

This serializes the operations and negates the benefits of threading.

**To Run:**
```bash
python bad_example.py