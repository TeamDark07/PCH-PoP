### 7.4: Using Non-Thread-Safe Components

A component (a class, object, or library) is considered **thread-safe** if it behaves correctly when accessed by multiple threads concurrently. Many components, especially those that maintain an internal state, are **not** thread-safe by default.

Using a non-thread-safe component from multiple threads without proper synchronization is a race condition. It can lead to corrupted internal state, incorrect results, and bizarre, hard-to-reproduce crashes.

**The Golden Rule:** Assume a component is **not** thread-safe unless its documentation explicitly guarantees that it is.

---

### 🔴 Bad Example (`bad_example.py`)

This script defines a simple `UnsafeDBClient` class that stores the last executed query in an instance variable (`self.last_query`).
1.  A single instance of this client is created.
2.  Multiple threads are started, and each thread is given a reference to this **same shared instance**.
3.  The threads call the `execute_query` method concurrently.
4.  This creates a race condition where one thread can overwrite `self.last_query` after another thread has set it but before it has been used, leading to data corruption.

**To Run:**
```bash
python bad_example.py