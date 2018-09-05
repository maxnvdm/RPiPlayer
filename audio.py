
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

led = 2

GPIO.setup(led, GPIO.OUT)
PWM = GPIO.PWM(led, 100)

try:
    PWM.start(50)
    on = False
    while True:
	    PWM.ChangeFrequency(200)
	    time.sleep(1)
	    PWM.ChangeFrequency(300)
	    time.sleep(1)
	    PWM.ChangeFrequency(400)
	    time.sleep(1)
	    PWM.ChangeDutyCycle(25)
	    time.sleep(1)
	    PWM.ChangeFrequency(300)
	    time.sleep(1)
	    PWM.ChangeFrequency(200)
	    time.sleep(1)
	    PWM.ChangeFrequency(100)


except KeyboardInterrupt:
        pass

PWM.stop()
GPIO.cleanup()