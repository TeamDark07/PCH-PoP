### 5.4: Using Threading Primitives in `asyncio`

The `threading` module and the `asyncio` module are two **separate and incompatible** concurrency paradigms. A common and critical mistake is to use synchronization primitives from the `threading` module (like `threading.Lock`) inside `asyncio` coroutines.

-   **`threading.Lock`:** This is a **blocking** primitive. When a coroutine calls `lock.acquire()`, it blocks the entire operating system thread. Since the `asyncio` event loop runs on that single thread, the entire application freezes.
-   **`asyncio.Lock`:** This is a **non-blocking**, or "cooperative," primitive. When a coroutine `await`s an `asyncio.Lock`, it registers its interest and then **yields control** to the event loop, allowing other tasks to run.

The rule is simple: **In `async` code, always use `asyncio` primitives.**

---

### 🔴 Bad Example (`bad_example.py`)

This script starts a background `fast_task` that prints a message every half-second to show if the event loop is responsive. It then starts two worker coroutines that compete for a shared `threading.Lock`. When one worker acquires the lock and enters a blocking `time.sleep()`, the event loop freezes, and the `fast_task` stops running.

**To Run:**
```bash
python bad_example.py