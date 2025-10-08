### 1.4: Dirty Read

A **dirty read** (or read skew) occurs when one thread reads data that has been partially modified by another thread but is not yet in a consistent state. This is common in multi-step transactions. If the writing thread were to fail and roll back, the reading thread would be left with invalid, "dirty" data that never officially existed.

This example simulates a bank transfer from one account to another, while a separate "audit" thread checks if the total money in the system remains constant.

---

### 🔴 Bad Example (`bad_example.py`)

In this script, the `transfer` function is not atomic. It debits one account, pauses briefly, and then credits the second account. The `audit` thread runs concurrently and can read the account balances during this pause. When it does, it sees an inconsistent state where money has momentarily "disappeared," flagging a dirty read.

**To Run:**
```bash
python bad_example.py