### 3.4: Priority Inversion

**Priority inversion** is a complex scheduling problem that occurs in priority-based systems. It happens when a high-priority task is indirectly blocked by a medium-priority task.

The scenario unfolds as follows:
1.  A **low-priority task** acquires a shared resource (like a lock).
2.  A **high-priority task** needs the same resource and is forced to wait (blocked).
3.  A **medium-priority task**, which does not need the resource, becomes ready to run.
4.  The scheduler sees that the high-priority task is blocked and the low-priority task is ready, but the medium-priority task has a higher priority than the low one. It "preempts" the low-priority task and runs the medium one instead.

The result: the medium-priority task is effectively blocking the high-priority task, "inverting" their priorities.

**Note:** Python's standard `threading` module doesn't offer real-time priority scheduling. These examples **simulate** this OS-level behavior to make the concept understandable.

---

### 🔴 Bad Example (`bad_example.py`)

This script uses `threading.Event`s and `time.sleep` to deterministically simulate the priority inversion problem.
-   The **low-priority** task acquires a lock.
-   The **high-priority** task starts and waits for the lock.
-   The **medium-priority** task starts. Our simulation models a scheduler that would now preempt the low-priority task. This is represented by a long `time.sleep(3)` inside the low-priority task's critical section, symbolizing the medium-priority task's execution time.
-   The high-priority task is forced to wait for this entire duration.

**To Run:**
```bash
python bad_example.py