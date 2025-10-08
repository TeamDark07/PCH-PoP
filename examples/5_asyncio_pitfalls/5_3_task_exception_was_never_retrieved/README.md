### 5.3: Task Exception Was Never Retrieved

When you schedule a coroutine to run as a background task with `asyncio.create_task()`, the event loop will run it concurrently. If that task raises an exception, the exception is not immediately raised in your main coroutine. Instead, it is stored inside the `Task` object.

If you never "retrieve" this exception,by awaiting the task or checking its `exception()` method,it will be lost, and the failure will be **silent**. This can lead to critical parts of your application failing without any visible error until the entire program is shutting down, at which point a final error message may be logged.

---

### 🔴 Bad Example (`bad_example.py`)

This script starts a `failing_background_task` using `asyncio.create_task()`. The main coroutine does not store the returned `Task` object and never awaits it. It simply continues with its own work and exits. The `ValueError` raised inside the task is never seen by the main logic.

**To Run:**
```bash
python bad_example.py