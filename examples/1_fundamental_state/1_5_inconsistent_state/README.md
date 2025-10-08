### 1.5: Inconsistent State / Partial Updates

An object is in an **inconsistent state** when its internal data violates its own rules or "invariants." This happens when a multi-step operation that modifies the object is interrupted, leaving the update only partially complete.

Unlike a "dirty read" (which is about *observing* a temporary bad state), this problem can leave the object permanently corrupted if the operation is not completed or rolled back.

This example uses a `GameCharacter` object whose `health` and `mana` must always sum to a constant value.

---

### 🔴 Bad Example (`bad_example.py`)

This script has multiple "worker" threads that randomly change the character's stats and one "checker" thread that constantly verifies the invariant (`health + mana == 100`). The `change_spec` method updates `health` and `mana` in two separate steps. If a thread is interrupted between these steps, the character is left in a broken state, which the checker thread will detect.

**To Run:**
```bash
python bad_example.py