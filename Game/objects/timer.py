import GLOBAL

import pygame

# TIMER CLASS
class Timer():
    def __init__(self):
        self.paused_tick = 0
        self.target_time = 0
        self.total_pause_ticks = 0
        self.start_pause_tick = -1
    
    # Returns current time and the target time with the pausing
    def start(self, start_time, time, reset_total_psue_tck = False):
        self.set_target_time(start_time, time)
        
        latest_pause_tick = self.paused_tick
        self.set_pause_tick()
        
        # The current pause tick - the latest grabbed pause tick
        new_pause_tick = self.paused_tick - latest_pause_tick
        
        # If the new pause tick isn't negative
        # Having it become negative will give you problems
        if new_pause_tick >= 0:
            # Add to target time and total pause ticks
            self.target_time += new_pause_tick
            self.total_pause_ticks += new_pause_tick
        
        if GLOBAL.current_tick > self.target_time:
            self.target_time = -1
            self.set_target_time(start_time, time)
            
            # Only used for timers that don't continously change the target time
            # Ex: lazer gun, shield
            # Not having this here would add unnessary extra time to systems that have a constant time to follow
            # This is not the case for the zone changer
            if reset_total_psue_tck:
                self.total_pause_ticks = 0
        
        return GLOBAL.current_tick, self.target_time
    
    # Sets the target time
    def set_target_time(self, start_time, time):
        if self.target_time <= 0:
            # Get the target time if the value is 0 or negative as it is the reset value
            
            # Total pause ticks is added so that the new target time can continue were the old
            # target time left off.
            self.target_time = start_time + time + self.total_pause_ticks
    
    # Sets the pause tick to allow pausing
    def set_pause_tick(self):
        
        if GLOBAL.paused:
            # Get the pause tick for this pause session
            self.start_pause_tick = self.get_start_time(self.start_pause_tick)
            
            self.paused_tick = GLOBAL.current_tick - self.start_pause_tick
        else:
            # The session is no longer paused stop grabing the pause tick
            self.start_pause_tick = -1
            
            self.paused_tick = 0
    
    # Returns a start time that doesn't update during a loop
    def get_start_time(self, start_time):
        if start_time < 0:
            start_time = GLOBAL.current_tick
        return start_time

    # Returns current time and the target time without the pausing
    def unpauseable_start(self, start_time, time):
        """
        The chad OG unpauseable timer    VS. The virgin difficult-to-implement pausable timer
                                          |
                     _O_/ Easy to         | A huge pain      _O     relies on GLOBAL.paused existance.
 Doesn't depend on  / |   understand.     | In the ass to   //|
 GLOBAL.paused     __/ \                  | set up.       __/\      I fixed the bug! no wait, 
                        \ Literally one   |                   \     I'm back where I started.
                          function.       |       needs to calculate the pause time.
        
        
        Hope you enjoyed this waste of time!
        """
        current_time = GLOBAL.current_tick
        target_time = start_time + time
        
        return current_time, target_time