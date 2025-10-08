### 7.2: Hybrid Concurrency Confusion

Mixing different concurrency models (`threading`, `multiprocessing`, `asyncio`) in the same application is an advanced technique that can lead to extremely subtle and hard-to-debug issues if not done with great care.

A common point of confusion is how to make a standard, synchronous thread interact with an `asyncio` event loop that is running in a different thread. The internal data structures of the `asyncio` event loop are **not thread-safe**. Calling a regular loop method from an external thread can corrupt the loop's state and cause a race condition.

---

### 🔴 Bad Example (`bad_example.py`)

This script runs an `asyncio` event loop in a background thread. It then starts a second, "external" thread that tries to schedule work on that loop by directly calling `loop.call_soon()`.

This is a **race condition**. The `call_soon` method is not designed to be called from a different thread. While this simple example might *appear* to work sometimes, in a real-world, high-load application, this unsafe call could lead to dropped tasks, corrupted internal state, or even a crash.

**To Run:**
```bash
python bad_example.py