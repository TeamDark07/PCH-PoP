### 3.2: Livelock

A **livelock** is a situation where two or more threads are actively running and changing state, but are not making any forward progress. Unlike a deadlock, where threads are blocked and waiting, livelocked threads are busy consuming CPU cycles while responding to each other's actions.

A classic analogy is two people trying to pass in a narrow hallway. They both politely step to the side, still blocking each other, then step back, and repeat the "polite dance" indefinitely.

---

### 🔴 Bad Example (`bad_example.py`)

This script simulates two "overly polite" workers that need to use a single shared resource to "eat."
1.  A worker picks up the resource.
2.  Before using it, it checks if the other worker is also trying to use it.
3.  If so, it politely puts the resource down to let the other worker go first.
4.  The other worker does the exact same thing.

This leads to a livelock where they continuously pick up and put down the resource, but neither ever gets to "eat."

**To Run:**
```bash
python bad_example.py