import phoenix
import time

rover = phoenix.Phoenix('192.168.1.11')
rover.start()

for i in range(100):
    #rover.setWheels(20,20)
    print(rover.temperature)
    time.sleep(0.1)
rover.setWheels(0,0)    
rover.close()