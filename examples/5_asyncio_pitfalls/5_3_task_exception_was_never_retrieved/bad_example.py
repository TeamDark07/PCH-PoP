# /examples/5_asyncio_pitfalls/5_3_task_exception_was_never_retrieved/bad_example.py

import asyncio
import time

async def failing_background_task():
    """
    A background task that is designed to fail.
    """
    print("[Task] Running in the background...")
    await asyncio.sleep(1)
    
    # This exception will be raised, but because no one is awaiting
    # this task, it will be "lost" until the program exits.
    print("[Task] Oh no, something went wrong!")
    raise ValueError("A critical error occurred in the task!")

async def main():
    print("--- 'Task Exception Was Never Retrieved' Demonstration ---")
    
    print("[Main] Starting a fire-and-forget background task that will fail.")
    
    # --- The Mistake is Here ---
    # We schedule the task to run, but we don't store the Task object
    # or ever await it. This is a "fire-and-forget" approach.
    asyncio.create_task(failing_background_task())
    
    print("[Main] Main coroutine is continuing without waiting for the task.")
    # The main coroutine will sleep, finish, and the program will exit.
    # The user will never see the ValueError from the background task.
    await asyncio.sleep(2)
    
    print("[Main] Main coroutine finished. The program appears to have succeeded.")
    print("[Main] Check the console output upon exit for a final error message.")

if __name__ == "__main__":
    asyncio.run(main())
    
    # A small sleep to give the finalizer a chance to print the error.
    time.sleep(0.1)