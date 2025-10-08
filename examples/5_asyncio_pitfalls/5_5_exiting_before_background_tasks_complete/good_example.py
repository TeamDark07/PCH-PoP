# /examples/5_asyncio_pitfalls/5_5_exiting_before_background_tasks_complete/good_example.py

import asyncio
import os

OUTPUT_FILE = "managed_task_output.txt"

async def slow_background_task(name):
    """
    A task that takes time to complete some important work.
    """
    print(f"[{name}] Starting important background work...")
    await asyncio.sleep(2)
    
    with open(f"{name}_{OUTPUT_FILE}", "a") as f:
        f.write(f"Task {name} completed.\n")
    
    print(f"[{name}] Background work finished.")

async def main():
    print("--- Correctly Managing Background Tasks ---")
    
    # Clean up files from previous runs
    for f in [f"TaskA_{OUTPUT_FILE}", f"TaskB_{OUTPUT_FILE}"]:
        if os.path.exists(f):
            os.remove(f)

    print("[Main] Scheduling two background tasks...")
    
    # --- The Solution is Here ---
    # 1. We create the tasks and store their handles.
    task_a = asyncio.create_task(slow_background_task("TaskA"))
    task_b = asyncio.create_task(slow_background_task("TaskB"))
    
    all_tasks = [task_a, task_b]
    
    print("[Main] Main coroutine is now waiting for all background tasks to complete...")
    
    # 2. We use asyncio.gather() to wait for all tasks in the list.
    #    The 'main' coroutine will pause here until both task_a and task_b
    #    have finished their work.
    await asyncio.gather(*all_tasks)
    
    print("[Main] All background tasks have finished. Main coroutine can now exit safely.")

if __name__ == "__main__":
    asyncio.run(main())
    
    print("\n--- Verification ---")
    task_a_exists = os.path.exists(f"TaskA_{OUTPUT_FILE}")
    task_b_exists = os.path.exists(f"TaskB_{OUTPUT_FILE}")
    
    if task_a_exists and task_b_exists:
        print("🟢 Both output files were created successfully.")
    else:
        print("🔴 One or more tasks did not complete.")