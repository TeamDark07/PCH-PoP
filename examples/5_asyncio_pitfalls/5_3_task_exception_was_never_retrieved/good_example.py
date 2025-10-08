# /examples/5_asyncio_pitfalls/5_3_task_exception_was_never_retrieved/good_example.py

import asyncio

async def failing_task(name):
    """A background task that fails after a short delay."""
    print(f"[{name}] Starting...")
    await asyncio.sleep(1)
    raise ValueError(f"Error in task {name}!")

def done_callback(task):
    """A callback function that checks for exceptions when a task is done."""
    print(f"[Callback] Task '{task.get_name()}' has finished.")
    if task.exception():
        print(f"[Callback] 🔴 Caught exception from task: {task.exception()}")

async def main():
    print("--- Correctly Handling Exceptions in Tasks ---")
    
    # --- Solution 1: Directly awaiting the task handle ---
    print("\n--- 1. Awaiting a single task ---")
    task1 = asyncio.create_task(failing_task("A"))
    try:
        # By awaiting the task, we allow its exception to propagate up.
        await task1
    except ValueError as e:
        print(f"[Main] 🟢 Caught expected exception from Task A: {e}")
        
    # --- Solution 2: Using asyncio.gather for multiple tasks ---
    print("\n--- 2. Using asyncio.gather ---")
    tasks = [
        asyncio.create_task(failing_task("B")),
        asyncio.create_task(failing_task("C")),
    ]
    try:
        # gather() runs all tasks concurrently. If any task raises an
        # exception, gather() will propagate the first one it encounters.
        await asyncio.gather(*tasks)
    except ValueError as e:
        print(f"[Main] 🟢 Caught expected exception from gather: {e}")
        # Note: You should handle task cancellation for the other tasks here
        # in a real application if one fails.
        for t in tasks:
            t.cancel()
            
    # --- Solution 3: Using a 'done callback' ---
    print("\n--- 3. Using a done callback ---")
    task2 = asyncio.create_task(failing_task("D"), name="D")
    # The callback will be executed when the task completes, regardless
    # of whether it succeeded or failed.
    task2.add_done_callback(done_callback)
    
    # Allow the task to run and the callback to fire.
    await asyncio.sleep(2)
    
    print("\nAll exception handling methods demonstrated.")

if __name__ == "__main__":
    asyncio.run(main())