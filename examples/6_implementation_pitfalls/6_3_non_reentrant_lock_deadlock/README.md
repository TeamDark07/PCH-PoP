### 6.3: Non-Reentrant Lock Deadlock

A **non-reentrant lock** (like `threading.Lock`) is a lock that cannot be acquired more than once by the same thread. If a thread acquires the lock and then tries to acquire it *again* before releasing it, it will get stuck waiting for itself. This is a form of deadlock.

This situation commonly occurs in object-oriented programming where one method of an object acquires a lock and then calls another method (or a helper function) on the same object that also needs to acquire the same lock.

---

### 🔴 Bad Example (`bad_example.py`)

This script demonstrates the deadlock using a standard `threading.Lock`.
1.  A `main_function` acquires the lock.
2.  While still holding the lock, it calls a `helper_function`.
3.  The `helper_function` attempts to acquire the very same lock.
4.  The thread immediately blocks. It is waiting for the lock to be released, but it is the one holding it. The program hangs.

**To Run:**
```bash
python bad_example.py