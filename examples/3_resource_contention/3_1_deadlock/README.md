### 3.1: Deadlock

A **deadlock** is a state in which two or more concurrent tasks are permanently blocked, each waiting for the other to release a resource. This creates a circular dependency that can never be resolved, causing the involved threads to hang forever.

The most common cause of a deadlock is when multiple threads try to acquire the same set of locks but in a different order.

---

### 🔴 Bad Example (`bad_example.py`)

This script demonstrates a classic deadlock scenario with two threads and two locks (`Lock A` and `Lock B`).

1.  **Worker 1** acquires `Lock A` and then tries to acquire `Lock B`.
2.  **Worker 2** acquires `Lock B` and then tries to acquire `Lock A`.

A `time.sleep()` is used to ensure that after Worker 1 gets Lock A, Worker 2 gets Lock B before Worker 1 can proceed. At this point, Worker 1 is waiting for Worker 2 to release Lock B, and Worker 2 is waiting for Worker 1 to release Lock A. They are stuck in a deadly embrace.

**To Run:**
```bash
python bad_example.py