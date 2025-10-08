# /examples/3_resource_contention/3_2_livelock/good_example.py

import threading
import time
import random

class SharedResource:
    def __init__(self):
        self.owner = None

class Worker(threading.Thread):
    def __init__(self, name, shared_resource, other_worker):
        super().__init__(name=name)
        self.shared_resource = shared_resource
        self.other_worker = other_worker
        self.dinners_eaten = 0

    def run(self):
        while self.dinners_eaten < 1:
            if self.shared_resource.owner is None:
                print(f"[{self.name}] Picking up the resource.")
                self.shared_resource.owner = self.name
            
            if self.shared_resource.owner == self.name:
                if self.other_worker.is_alive() and self.other_worker.dinners_eaten < 1:
                    print(f"[{self.name}] sees {self.other_worker.name} needs the resource, yielding.")
                    self.shared_resource.owner = None
                    
                    # --- The Solution: Randomized Backoff ---
                    # Instead of immediately retrying, wait for a small,
                    # random amount of time. This breaks the symmetry of the
                    # livelock, making it highly probable that one thread will
                    # retry when the other is still sleeping.
                    time.sleep(random.uniform(0.1, 0.5))
                else:
                    print(f"[{self.name}] is finally eating!")
                    self.dinners_eaten += 1
                    self.shared_resource.owner = None
            
            time.sleep(0.1)

if __name__ == "__main__":
    resource = SharedResource()
    worker1 = Worker(name="Worker-A", shared_resource=resource, other_worker=None)
    worker2 = Worker(name="Worker-B", shared_resource=resource, other_worker=None)
    worker1.other_worker = worker2
    worker2.other_worker = worker1
    
    print("--- Livelock Avoidance Example ---")
    print("Workers use randomized backoff to break the cycle.")
    
    worker1.start()
    worker2.start()
    
    # No timeout needed; the threads will now finish.
    worker1.join()
    worker2.join()
    
    print("\nAll workers finished successfully. Livelock was avoided.")