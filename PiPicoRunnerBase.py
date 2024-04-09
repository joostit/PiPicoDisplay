#################################################################################
# Copyright (c) 2024 DevOats
# The MIT License
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#################################################################################
#
# PiPicoRunnerBase
# Author: Joost/DevOats
# A Simple Base class to easily run micropython projects with configurable fast and a slow periodical Ticks.
# Both Ticks are separately protected against multiple execution and are only called if the previous call has finished executing
#
# 
# Usage:
#   - Inherit from this base class
#   - Call the super constructor from your constructor
#   - Override the following methods:
#      - fastTick(self)   (optional)
#      - slowTick(self)   (optional)
#      - beforeRun(self)  (optional)
#
#   - In the beforeRun override, set the following configuration variables: (optional)
#      - piPicoRunnerBase.runSlowTickOnSecondCore = [True]/False  -->  Sets whether the Slow tick gets called on the second CPU core
#      - piPicoRunnerBase.slowTickFrequency = [20]                -->  Sets the Slow tick timer frequency
#      - piPicoRunnerBase.fastTickFrequency = [1000]              -->  Sets the Fast tick timer frequency
#
#   - Call the run() method. Not that this method does not return. All custom application logic should be put
#     in the beforeRun, fastTick and slowTick methods for the inheriting class.
#
#
#

from machine import Timer
import _thread
import time

class piPicoRunnerBase:
    
    
    # Override this method to be called periodically on the slow tick frequency
    def fastTick(self):
        pass
    
    
    # Override this method to be called periodically on the slow tick frequency
    # Depending on configuration, this can be executed be on the second CPU Core
    def slowTick(self):
        pass
    
    
    # Override this method to initialize stuff before the Tick Timers are started.
    # This method will be called when startRun is called.
    def beforeRun(self):
        pass
    
    
    # Call this method from you script entry point (__main__) to start execution
    # Note that this method does NOT return. All application logic should be executed in the child class method
    def run(self):
        self.beforeRun()
        print("Starting Tick timers")
        self.__fastTickTimer.init(freq=self.fastTickFrequency, mode=Timer.PERIODIC, callback=self.__fastTickTimerCallback)
        self.__slowTickTimer.init(freq=self.slowTickFrequency, mode=Timer.PERIODIC, callback=self.__slowTickTimerCallback)
        
        #Endless loop to prevent the script from exiting
        while True:
            time.sleep(2)
    
    
    # Constructor. Must be explicitly called from the child class
    def __init__(self):
        self.runSlowTickOnSecondCore = True  # Set this to True to let the slow tick run on the second CPU core
        self.slowTickFrequency = 20          # Sets the Slow tick timer frequency
        self.fastTickFrequency = 1000        # Sets the Fast tick timer frequency
        
        self.__slowTickRunning = False    # Is true while the slow Tick is running. (To prevent two update triggers running simultanious, when the first one takes too long)
        self.__fastTickRunning = False    # Is true while the fast Tick is running. (To prevent two update triggers running simultanious, when the first one takes too long)
        
        print("Initializing Pi Pico Runner Base")
        self.__fastTickTimer = Timer()
        self.__slowTickTimer = Timer()
        
        
    # Callback for the fast tick timer
    def __fastTickTimerCallback(self, timer):
        if not self.__fastTickRunning:
            self.__fastTickRunning = True
            self.fastTick()
            self.__fastTickRunning = False

    
    #Callback for the slow tick timer
    def __slowTickTimerCallback(self, timer):
        if not self.__slowTickRunning:
            self.__slowTickRunning = True
            
            if self.runSlowTickOnSecondCore:
                _thread.start_new_thread(self.__slowtickThreadRunner, ())
            else:
                self.__slowtickThreadRunner()
    
    
    # Runs the slow tick on the second processor core, or on core 1, depending on configuration
    def __slowtickThreadRunner(self):
        self.slowTick()
        self.__slowTickRunning = False
        
