### 5.1: Blocking the Event Loop

The single most important rule in `asyncio` is: **never block the event loop.**

`asyncio` uses a single-threaded event loop for cooperative multitasking. This means that for one coroutine to run, another must voluntarily give up control. If any coroutine performs a synchronous, blocking operation (like `time.sleep()`, a standard network request, or a long CPU-bound calculation), it freezes the entire event loop. No other tasks can run until the blocking call is complete.

---

### 🔴 Bad Example (`bad_example.py`)

This script starts two tasks concurrently: a `fast_task` that prints a message every second, and a `slow_blocking_task` that calls the synchronous `time.sleep(5)`.

When the slow task is running, the `time.sleep(5)` call blocks the entire thread. As a result, the event loop is frozen, and the `fast_task` is starved and cannot run.

**To Run:**
```bash
python bad_example.py