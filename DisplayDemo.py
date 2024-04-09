from machine import Pin, Timer
from PiPicoRunnerBase import piPicoRunnerBase
import PicoOled13

import machine


class DisplayDemo(piPicoRunnerBase):

    # Overrides the base class method to do initializations
    def beforeRun(self):
        print("Runnning")
        piPicoRunnerBase.runSlowTickOnSecondCore = True
        piPicoRunnerBase.slowTickFrequency = 20          # Sets the Slow tick timer frequency
        piPicoRunnerBase.fastTickFrequency = 1000        # Sets the Fast tick timer frequency
        
        self.blinkTimer = Timer()
        self.blinkTimer.init(freq=2, mode=Timer.PERIODIC, callback=self.blink)


    # Constructor
    def __init__(self):
        super().__init__()     # Mandatory to get the base class to work
        
        self.display=PicoOled13.get()
        self.display.clear()

        self.buttonACnt = 0             # Counts KEY0 presses
        self.buttonBCnt = 0             # Counts KEY1 presses

        self.runCnt = 0                 # Counts the number of display updates (For debug purposes)

        self.btnAPressed = False        # True if KEY0 is pressed down
        self.btnBPressed = False        # True if KEY1 is pressed 

        self.updateDisplay = True       # Set to True if the Display needs to be updated in the next update cycle
        
        self.led = machine.Pin("LED", machine.Pin.OUT)
        self.led.on()


    # Gets called by the base class to run on the fast tick frequency intervals.
    # Runs the button logic
    def fastTick(self):
        self.checkBtnA()
        self.checkBtnB()
    
    # Checks the state of KEY0 and updates the counter if needed
    def checkBtnA(self):
        if not self.btnAPressed:
            if self.display.is_pressed(self.display.KEY0):
                self.btnAPressed = True
                self.buttonACnt += 1
                self.updateDisplay = True
        else:
            if not self.display.is_pressed(self.display.KEY0):
                self.btnAPressed = False

    
    # Checks the state of KEY1 and updates the counter if needed
    def checkBtnB(self):
        if not self.btnBPressed:
            if self.display.is_pressed(self.display.KEY1):
                self.btnBPressed = True
                self.buttonBCnt += 1
                self.updateDisplay = True
        else:
            if not self.display.is_pressed(self.display.KEY1):
                self.btnBPressed = False
    

    # Gets called by the base class to run on the slow tick frequency intervals
    # Runs the display logic
    def slowTick(self):
        self.runCnt +=1 

        if self.updateDisplay:
            self.updateDisplay  = False
            self.display.clear(False)
            self.display.text("Key0: " + str(self.buttonACnt) , 0,0)
            self.display.text("Key1: " + str(self.buttonBCnt) , 0,15)
            self.display.text(str(self.runCnt) , 100,55)
            self.display.show(0, 23)
            

    # Gets called by the BlinkTimer to toggle the onboard LED on the Pi Pico
    def blink(self, timer):
        self.led.toggle()


# Application runs from here
if __name__ == '__main__':
    runner = DisplayDemo()
    runner.run()
