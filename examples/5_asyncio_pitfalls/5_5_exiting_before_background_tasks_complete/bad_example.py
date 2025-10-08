# /examples/5_asyncio_pitfalls/5_5_exiting_before_background_tasks_complete/bad_example.py

import asyncio
import os

OUTPUT_FILE = "background_task_output.txt"

async def slow_background_task():
    """
    A task that takes time to complete some important work.
    """
    print("[Task] Starting important background work...")
    await asyncio.sleep(2) # Simulate a long I/O operation
    
    # This critical write operation will likely be cancelled before it can run.
    with open(OUTPUT_FILE, "w") as f:
        f.write("Background work completed successfully.")
    
    print("[Task] Background work finished.")

async def main():
    print("--- Exiting Before Background Tasks Complete ---")
    
    # Clean up file from previous runs
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    print("[Main] Scheduling a slow background task (fire-and-forget).")
    
    # --- The Mistake is Here ---
    # We create the task, but the 'main' coroutine does not wait for it.
    asyncio.create_task(slow_background_task())
    
    print("[Main] Main coroutine has finished its own work and is exiting now.")
    # When 'main' returns, asyncio.run() will shut down the event loop.
    # The running 'slow_background_task' will be cancelled at whatever
    # point it was in its execution (likely during the sleep).

if __name__ == "__main__":
    asyncio.run(main())
    
    print("\n--- Verification ---")
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r') as f:
            content = f.read()
        print(f"File content: '{content}'")
    else:
        print("🔴 The output file was never created.")
        print("The background task was cancelled before it could finish its work.")