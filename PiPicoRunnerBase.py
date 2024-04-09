# PiPicoRunnerBase
# A Simple Base class to easily run simple micropython projects with both a fast and a slow periodical Tick.
# Author: OatShort
# 
# 
# Usage:
#   - Override this base class
#   - Call the super constructor from your constructor
#
#

from machine import Timer

class piPicoRunnerBase:
    
    def __init__(self):
        print("Initializing Pi Pico Runner Base")
        self.fastloopTimer = Timer()
        self.displayTimer = Timer()
        
        
        
    def loopFastTriggered(self, timer):
        self.fastTick()


    def loopSlowTriggered(self, timer):
        self.slowTick()
        
        
    def fastTick(self):
        pass    
    
    
    def slowTick(self):
        pass
        
        
    def startRun(self):
        self.beforeRun()
        print("Starting Tick timers")
        self.fastloopTimer.init(freq=1000, mode=Timer.PERIODIC, callback=self.loopFastTriggered)
        self.displayTimer.init(freq=20, mode=Timer.PERIODIC, callback=self.loopSlowTriggered)
        
        
    # Override this method to initialize stuff before the Tick Timers are started
    def beforeRun(self):
        pass
        
        
    


        
