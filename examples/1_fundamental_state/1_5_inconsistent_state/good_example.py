# /examples/1_fundamental_state/1_5_inconsistent_state/good_example.py

import threading
import time
import random

# Global event to signal threads to stop
stop_event = threading.Event()

class GameCharacter:
    """
    A thread-safe character class.
    A lock protects the invariant: health + mana must always equal MAX_POWER.
    """
    MAX_POWER = 100

    def __init__(self, name, health=50):
        self.name = name
        self.health = health
        self.mana = self.MAX_POWER - health
        self.lock = threading.Lock()

    def change_spec(self, new_health):
        """
        Changes the character's spec atomically using a lock.
        """
        new_mana = self.MAX_POWER - new_health
        
        with self.lock:
            # The entire update is now a single, indivisible operation.
            # No other thread can see the character's state while it is
            # being modified inside this 'with' block.
            self.health = new_health
            time.sleep(0.001)
            self.mana = new_mana

    def check_consistency(self):
        """
        Checks if the character's state is valid. It also acquires the lock
        to ensure it reads a consistent snapshot.
        """
        with self.lock:
            if self.health + self.mana != self.MAX_POWER:
                print("--- INCONSISTENCY DETECTED! THIS SHOULD NOT HAPPEN ---")
                stop_event.set()
                return False
        return True

def worker(character):
    """A thread that randomly changes the character's spec."""
    while not stop_event.is_set():
        new_health = random.randint(1, 99)
        character.change_spec(new_health)

def consistency_checker(character):
    """A thread that continuously checks the character's state."""
    while not stop_event.is_set():
        if not character.check_consistency():
            break # Exit if an error is found
        time.sleep(0.0001)

if __name__ == "__main__":
    player = GameCharacter("Gandalf")
    
    threads = []
    for _ in range(5):
        threads.append(threading.Thread(target=worker, args=(player,)))
    threads.append(threading.Thread(target=consistency_checker, args=(player,)))

    for t in threads:
        t.start()

    # Let the simulation run for a couple of seconds
    time.sleep(2)
    stop_event.set() # Signal all threads to stop

    for t in threads:
        t.join()

    print("Simulation finished. The character's state remained consistent throughout.")
    print(f"Final state: Health={player.health}, Mana={player.mana}, Total={player.health + player.mana}")