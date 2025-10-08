### 3.3: Starvation

**Starvation** (or indefinite postponement) occurs when a thread is perpetually denied access to a shared resource it needs to make progress. While other "greedy" threads are able to repeatedly access the resource, the starved thread is constantly overlooked by the scheduler.

This can happen even with a standard `threading.Lock` because the lock does not guarantee the order in which waiting threads will acquire it. If there's high contention, a thread might get unlucky and be ignored indefinitely.

---

### 🔴 Bad Example (`bad_example.py`)

This script simulates a high-contention environment with several "greedy" workers that constantly acquire and release a lock. A single "patient" worker tries to acquire the same lock just once to perform a critical task.

Due to the aggressive competition from the greedy workers, there's a high probability that the patient worker's request will be repeatedly overlooked, and it will "starve."

**To Run:**
```bash
python bad_example.py