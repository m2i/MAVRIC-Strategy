import phoenix
import time
import random

rover = phoenix.Phoenix('192.168.1.11')
rover.open()
target = random.randrange(100)/100.
print(target)
time.sleep(1)
if (rover.actuator - target > 0.1):
    rover.setActuator(-1)
elif (rover.actuator - target < 0.1):
    rover.setActuator(1)
for i in range(100):
    rover.setWheels(20,20)
    try:
        if (abs(rover.actuator - target) < 0.01):
            rover.setActuator(0)
        print('T: %f C, A: %f' % (rover.temperature, rover.actuator))
    except:
        pass
    time.sleep(0.1)
rover.setWheels(0,0)
rover.setActuator(0)    
rover.close()