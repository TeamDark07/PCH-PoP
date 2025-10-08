# /examples/4_system_challenges/4_7_signal_handling_in_multiprocessing/good_example.py

import multiprocessing
import time
import os
import signal

# We will use a Pool, which has better built-in signal handling.
# However, we will also show a manual approach for a single Process.

def worker_process(some_arg):
    """
    A worker process that is now aware it might be terminated.
    Note: 'finally' blocks are not guaranteed to run on SIGTERM,
    so critical cleanup should be handled by the parent.
    """
    # Set a signal handler to ignore SIGINT so the parent can manage shutdown.
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    
    print(f"[Worker PID: {os.getpid()}] Starting work. Press Ctrl+C.")
    
    try:
        for i in range(10):
            print(f"[Worker PID: {os.getpid()}] Working... ({i+1}/10)")
            time.sleep(1)
        print(f"[Worker PID: {os.getpid()}] Finished work normally.")
    except Exception as e:
        print(f"[Worker PID: {os.getpid()}] Encountered an error: {e}")


class GracefulKiller:
    """A class to handle signals and trigger a graceful shutdown."""
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        print(f"\n[Main PID: {os.getpid()}] Signal {signum} received. Triggering shutdown.")
        self.kill_now = True


if __name__ == "__main__":
    print(f"[Main PID: {os.getpid()}] Starting worker process with graceful shutdown handler.")
    
    killer = GracefulKiller()
    
    # Using a Pool is often the best practice as it has more robust shutdown logic.
    # We will use one process in the pool for this example.
    pool = multiprocessing.Pool(processes=1)
    
    # Start the worker asynchronously.
    result = pool.apply_async(worker_process, args=("some_arg",))
    
    # Wait for the worker to finish or for a shutdown signal.
    while not result.ready():
        if killer.kill_now:
            print("[Main PID] Shutdown signal detected. Terminating the pool.")
            # The pool.terminate() sends SIGTERM to the child process.
            pool.terminate()
            pool.join()
            print("[Main PID] Pool terminated. Main process is exiting.")
            break
        
        # We use a timed wait to remain responsive to signals.
        result.wait(timeout=1.0)
    else: # This 'else' belongs to the 'while' loop. It runs if the loop finishes without a 'break'.
        print("[Main PID] Worker finished its job normally.")
        pool.close()
        pool.join()

    print("\nProgram exited cleanly.")