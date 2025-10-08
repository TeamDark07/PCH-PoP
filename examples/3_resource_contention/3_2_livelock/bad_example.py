# /examples/3_resource_contention/3_2_livelock/bad_example.py

import threading
import time

class SharedResource:
    """A resource that can be owned by one worker at a time."""
    def __init__(self):
        self.owner = None

class Worker(threading.Thread):
    def __init__(self, name, shared_resource, other_worker):
        super().__init__(name=name)
        self.shared_resource = shared_resource
        self.other_worker = other_worker
        self.dinners_eaten = 0

    def run(self):
        while self.dinners_eaten < 1: # Try to eat one dinner
            # --- The Livelock Logic is Here ---
            
            # 1. Take the resource if it's free.
            if self.shared_resource.owner is None:
                print(f"[{self.name}] Picking up the resource.")
                self.shared_resource.owner = self.name
            
            # 2. If I own the resource, check if the other worker is trying to work.
            if self.shared_resource.owner == self.name:
                # This is the "overly polite" step.
                if self.other_worker.is_alive(): # Simplified check for "is other hungry?"
                    print(f"[{self.name}] sees {self.other_worker.name} is also working, putting resource down.")
                    self.shared_resource.owner = None
                else:
                    # Success!
                    print(f"[{self.name}] is finally eating!")
                    self.dinners_eaten += 1
                    self.shared_resource.owner = None # Put it down when done
            
            # Small sleep to prevent burning 100% CPU and to make the livelock visible
            time.sleep(0.1)

if __name__ == "__main__":
    resource = SharedResource()
    
    # Create two workers. Note that we can't set the other_worker yet.
    worker1 = Worker(name="Worker-A", shared_resource=resource, other_worker=None)
    worker2 = Worker(name="Worker-B", shared_resource=resource, other_worker=None)
    
    # Now that both exist, they can reference each other.
    worker1.other_worker = worker2
    worker2.other_worker = worker1
    
    print("--- Livelock Example ---")
    print("Two 'polite' workers will constantly yield the resource to each other.")
    
    worker1.start()
    worker2.start()
    
    # Use a timeout because the threads will livelock and never finish.
    worker1.join(timeout=3)
    worker2.join(timeout=3)
    
    if worker1.is_alive() or worker2.is_alive():
        print("\nLIVELOCK DETECTED! The workers are active but making no progress.")
    else:
        print("\nWorkers finished (this should not happen in a livelock).")