from machine import Pin, Timer
import PicoOled13
import _thread
import machine
import time


class Main(object):

    def run(self):
        print("Runnnig")
        self.btnTimer = Timer()
        self.btnTimer.init(freq=1000, mode=Timer.PERIODIC, callback=self.btnLoop)

        self.displayTimer = Timer()
        self.displayTimer.init(freq=2, mode=Timer.PERIODIC, callback=self.displayLoop)

        self.timer = Timer()
        self. timer.init(freq=2, mode=Timer.PERIODIC, callback=self.blink)

    def __init__(self):
        self.display=PicoOled13.get()
        self.display.clear()

        self.buttonACnt = 0
        self.buttonBCnt = 0

        self.runCnt = 0

        self.btnAPressed = False
        self.btnBPressed = False

        self.updateDisplay = True

        self.led = machine.Pin("LED", machine.Pin.OUT)
        self.led.on()


    def btnLoop(self, timer):
        if not self.btnAPressed:
            if self.display.is_pressed(self.display.KEY0):
                self.btnAPressed = True
                self.buttonACnt += 1
                self.updateDisplay = True
        else:
            if not self.display.is_pressed(self.display.KEY0):
                self.btnAPressed = False
    

    def displayLoop(self,timer):
        _thread.start_new_thread(self.displayThread, ())
        

    def displayThread(self):

        self.runCnt +=1 

        if self.updateDisplay:
            self.updateDisplay  = False
            self.display.clear()
            self.display.text("Key0: " + str(self.buttonACnt) , 0,0)
            self.display.text("Key1: " + str(self.buttonBCnt) , 0,15)
            self.display.text(str(self.runCnt) , 100,55)
            self.display.show()


    def blink(self, timer):
        self.led.toggle()


if __name__ == '__main__':
    runner = Main()
    runner.run()

    #Endless loop to prevent script from exiting
    while True:
        time.sleep(2)

