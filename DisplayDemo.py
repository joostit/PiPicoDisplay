from machine import Pin, Timer
import PicoOled13
import _thread
import machine
import time


class DisplayDemo(object):

    # Main run method for the Display Demo
    def run(self):
        print("Runnning")
        self.fastloopTimer = Timer()
        self.fastloopTimer.init(freq=1000, mode=Timer.PERIODIC, callback=self.fastLoopTriggered)

        self.displayTimer = Timer()
        self.displayTimer.init(freq=20, mode=Timer.PERIODIC, callback=self.displayTimerTriggered)

        self.blinkTimer = Timer()
        self.blinkTimer.init(freq=2, mode=Timer.PERIODIC, callback=self.blink)


    # Constructor
    def __init__(self):
        self.display=PicoOled13.get()
        self.display.clear()

        self.buttonACnt = 0             # Counts KEY0 presses
        self.buttonBCnt = 0             # Counts KEY1 presses

        self.runCnt = 0                 # Counts the number of display updates (For debug purposes)

        self.btnAPressed = False        # True if KEY0 is pressed down
        self.btnBPressed = False        # True if KEY1 is pressed 

        self.updateDisplay = True       # Set to True if the Display needs to be updated in the next update cycle
        self.displayUpdating = False    # Is true while the display is updated. (To prevent two update triggers running simultanious, when the first one takes too long)

        self.led = machine.Pin("LED", machine.Pin.OUT)
        self.led.on()


    # Gets called every 1ms by the fastloopTimer. Put application logic here
    def fastLoopTriggered(self, timer):
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
    

    #Gets called by the DisplayTimer to update the display
    def displayTimerTriggered(self,timer):
        if not self.displayUpdating:
            self.displayUpdating = True
            _thread.start_new_thread(self.displayUpdateThreadRunner, ())


    # Runs the display update logic on the second processor core
    def displayUpdateThreadRunner(self):
            self.runCnt +=1 

            if self.updateDisplay:
                self.updateDisplay  = False
                self.display.clear(False)
                self.display.text("Key0: " + str(self.buttonACnt) , 0,0)
                self.display.text("Key1: " + str(self.buttonBCnt) , 0,15)
                self.display.text(str(self.runCnt) , 100,55)
                self.display.show(0, 23)
            self.displayUpdating = False


    # Gets called by the BlinkTimer to toggle the onboard LED on the Pi Pico
    def blink(self, timer):
        self.led.toggle()


# Demo runs from here
if __name__ == '__main__':
    runner = DisplayDemo()
    runner.run()

    #Endless loop to prevent the script from exiting
    while True:
        time.sleep(2)

