### 5.5: Exiting Before Background Tasks Complete

When the main coroutine of an `asyncio` program finishes, the `asyncio.run()` function will proceed to shut down the event loop. As part of this shutdown process, it will find any still-running tasks that were created with `asyncio.create_task()` and **cancel** them.

This can lead to silent failures where critical background work is started but never completed, as the program exits before the tasks have a chance to finish.

---

### 🔴 Bad Example (`bad_example.py`)

This script schedules a `slow_background_task` that needs 2 seconds to complete and write to a file. The `main` coroutine, however, does not wait for it. It schedules the task and then immediately finishes. The `asyncio.run()` function then cancels the still-sleeping background task before it can write to the file.

**To Run:**
```bash
python bad_example.py