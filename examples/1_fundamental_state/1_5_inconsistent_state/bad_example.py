# /examples/1_fundamental_state/1_5_inconsistent_state/bad_example.py

import threading
import time
import random

# Global event to signal when an inconsistency is found
inconsistency_found = threading.Event()

class GameCharacter:
    """
    A character with health and mana.
    This class has an important invariant: health + mana must always equal MAX_POWER.
    """
    MAX_POWER = 100

    def __init__(self, name, health=50):
        self.name = name
        self.health = health
        self.mana = self.MAX_POWER - health

    def change_spec(self, new_health):
        """
        Changes the character's spec. This operation is NOT atomic and can be
        interrupted, leaving the character in an inconsistent state.
        """
        new_mana = self.MAX_POWER - new_health
        
        # --- Critical Section Start ---
        # Step 1: Update health
        self.health = new_health
        
        # A context switch here is disastrous.
        # The health has changed, but the mana has not.
        # The invariant (health + mana == 100) is now broken.
        time.sleep(0.001) 
        
        # Step 2: Update mana
        self.mana = new_mana
        # --- Critical Section End ---

    def check_consistency(self):
        """Checks if the character's state is valid."""
        if self.health + self.mana != self.MAX_POWER:
            print("--- INCONSISTENCY DETECTED! ---")
            print(f"Health: {self.health}, Mana: {self.mana}, Total: {self.health + self.mana}")
            inconsistency_found.set()

def worker(character):
    """A thread that randomly changes the character's spec."""
    while not inconsistency_found.is_set():
        new_health = random.randint(1, 99)
        character.change_spec(new_health)

def consistency_checker(character):
    """A thread that continuously checks the character's state."""
    while not inconsistency_found.is_set():
        character.check_consistency()
        time.sleep(0.0001)

if __name__ == "__main__":
    player = GameCharacter("Gandalf")
    
    threads = []
    # Create threads to modify the character's state
    for _ in range(5):
        threads.append(threading.Thread(target=worker, args=(player,)))
    
    # Create a dedicated thread to check for consistency
    threads.append(threading.Thread(target=consistency_checker, args=(player,)))

    for t in threads:
        t.start()

    # Let the simulation run for a short time or until an error is found
    inconsistency_found.wait(timeout=2) # Wait for 2 seconds

    # Stop all threads
    inconsistency_found.set()
    for t in threads:
        t.join()

    if player.health + player.mana == GameCharacter.MAX_POWER:
        print("Simulation finished. No inconsistency was detected in time.")
    else:
        print("Simulation finished. The character was left in an inconsistent state.")