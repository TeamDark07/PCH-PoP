# /examples/5_asyncio_pitfalls/5_2_coroutine_was_never_awaited/good_example.py

import asyncio

async def important_task(name):
    """Simulates an important task that needs to be run."""
    print(f"Starting task '{name}'...")
    await asyncio.sleep(1)
    print(f"Task '{name}' has finished!")

async def main():
    print("--- Correctly Running Coroutines ---")
    
    # --- Solution 1: Using 'await' ---
    # 'await' tells the event loop to run the coroutine and to pause
    # the 'main' function until 'important_task' is complete.
    print("\nRunning a coroutine with 'await':")
    await important_task("A (awaited)")
    
    print("\n-----------------------------------\n")
    
    # --- Solution 2: Using 'asyncio.create_task()' for concurrency ---
    # 'create_task' schedules the coroutine to run on the event loop
    # as a background task. It returns a Task object immediately, and
    # the 'main' function can continue doing other work.
    print("Running two coroutines concurrently with 'asyncio.create_task()':")
    task_b = asyncio.create_task(important_task("B (background)"))
    task_c = asyncio.create_task(important_task("C (background)"))
    
    print("Main function continues while background tasks are running...")
    
    # It's crucial to wait for the background tasks to finish before
    # the program exits. We do this by awaiting the Task objects.
    await task_b
    await task_c
    
    print("\nAll tasks have completed successfully.")

if __name__ == "__main__":
    asyncio.run(main())