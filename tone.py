
# defines
PORT = 5678

import sys, time, os
sys.path.append('/home/pi/tone/lib') # set search path

import t_motion, t_osc
import t_io as io
import setup

# Sensor Instanciate
motion = t_motion.Motion()
system = setup.System()
# OSC Instanciate
osc = t_osc.Osc(system.send_ip, PORT)
#INIT Modules
motion.setup()
io.setup()

# Main Loop
print("Start main loop...")
try:
    while(1):
        motion.update()
        io.update()
        # print(io.get_bt_state())
        # print(motion.speed)

        if io.get_bt_state() == 1:
            osc.send("bt", 1)
        else:
            osc.send("bt", 0)

        time.sleep(0.005) #0.005

except KeyboardInterrupt:
    pass
