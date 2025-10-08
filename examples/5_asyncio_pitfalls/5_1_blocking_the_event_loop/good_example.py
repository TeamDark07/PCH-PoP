# /examples/5_asyncio_pitfalls/5_1_blocking_the_event_loop/good_example.py

import asyncio
import time

async def fast_task():
    """A coroutine that runs frequently."""
    while True:
        print("Fast task is running...")
        try:
            # This is a checkpoint where the task can be cancelled.
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            print("Fast task was cancelled.")
            break

async def slow_non_blocking_task():
    """
    Solution 1: Use the asynchronous version of the blocking call.
    """
    print("Slow (but non-blocking) task started, will yield control for 5 seconds.")
    
    # --- The Correct Approach ---
    # asyncio.sleep() is a non-blocking call. It tells the event loop,
    # "Pause this coroutine for 5 seconds, but feel free to run other tasks
    # in the meantime."
    await asyncio.sleep(5)
    
    print("Slow (but non-blocking) task finished.")

def truly_blocking_function():
    """
    A regular synchronous function that is unavoidably slow.
    This could be a CPU-bound calculation or a call to a legacy library.
    """
    print("[Executor] Starting a genuinely blocking function in a separate thread...")
    time.sleep(5)
    print("[Executor] Blocking function finished.")
    return "Done"

async def main():
    """The main entry point, demonstrating both solutions."""
    
    print("--- Avoiding Blocking the Event Loop ---")
    
    fast_task_handle = asyncio.create_task(fast_task())
    await asyncio.sleep(0.1)
    
    # --- Solution 1: Using async equivalent ---
    print("\n--- Running a non-blocking async sleep ---")
    await slow_non_blocking_task()
    
    print("\nObserve the output:")
    print("The 'Fast task is running...' message NEVER stopped appearing.")
    print("This is because `await asyncio.sleep()` yielded control correctly.")
    
    # --- Solution 2: Running blocking code in an executor ---
    print("\n--- Running a truly blocking function in a thread pool executor ---")
    loop = asyncio.get_running_loop()
    
    # `run_in_executor` offloads the blocking function to a separate thread,
    # keeping the event loop free to run other tasks.
    result = await loop.run_in_executor(
        None, # Use the default ThreadPoolExecutor
        truly_blocking_function
    )
    
    print("\nObserve the output again:")
    print("The 'Fast task is running...' message NEVER stopped appearing.")
    print(f"The executor returned the result: '{result}'")

    # Cleanly stop the fast task
    fast_task_handle.cancel()
    await fast_task_handle

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program exited.")