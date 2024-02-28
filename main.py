from machine import Pin, Timer
import PicoOled13
import _thread

display=PicoOled13.get()
display.clear()

display.text("Nothing is pressed",0,0,0xffff)

buttonACnt = 0
buttonBCnt = 0

runCnt = 0

btnAPressed = False
btnBPressed = False

updateDisplay = True

led = machine.Pin("LED", machine.Pin.OUT)
led.on()

def btnLoop(timer):
    global btnAPressed
    global buttonACnt
    global updateDisplay

    if not btnAPressed:
        if display.is_pressed(display.KEY0):
            btnAPressed = True
            buttonACnt += 1
            updateDisplay = True
    else:
        if not display.is_pressed(display.KEY0):
            btnAPressed = False
    
    
def displayLoop(timer):
    _thread.start_new_thread(displayThread, ())
    
def displayThread():
    global runCnt
    global updateDisplay
    global buttonACnt
    global buttonBCnt
    
    runCnt +=1 

    if updateDisplay:
        updateDisplay  = False
        display.clear()
        display.text("Key0: " + str(buttonACnt) , 0,0)
        display.text("Key1: " + str(buttonBCnt) , 0,15)
        display.text(str(runCnt) , 100,55)
        display.show()

def blink(timer):
    led.toggle()

btnTimer = Timer()
btnTimer.init(freq=1000, mode=Timer.PERIODIC, callback=btnLoop)

displayTimer = Timer()
displayTimer.init(freq=2, mode=Timer.PERIODIC, callback=displayLoop)

timer = Timer()
timer.init(freq=2, mode=Timer.PERIODIC, callback=blink)
