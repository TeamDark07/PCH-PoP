### 5.2: Coroutine Was Never Awaited

In `asyncio`, a function defined with `async def` is a **coroutine function**. When you call it, it does **not** run the code inside. Instead, it returns a **coroutine object**.

This object is like a blueprint for a task. It does nothing until you explicitly tell the `asyncio` event loop to run it. Forgetting to do so is a very common mistake that leads to code silently failing to execute. The only clue is a `RuntimeWarning` that Python prints when the program exits.

---

### 🔴 Bad Example (`bad_example.py`)

This script defines an `async` function `important_task()`. The `main` function then calls it like a regular function: `important_task()`. This creates a coroutine object, but it is never passed to the event loop, so its code is never executed.

**To Run:**
```bash
python bad_example.py