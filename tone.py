import sys, time, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + './lib') # set search path
import t_motion
import t_io as io


motion = t_motion.Motion()
motion.setup()
io.setup()

try:
    while(1):
        m.update()
        io.update()
        print(io.get_bt_state())

        io.led_on()
        io.led_off()
        # print(m.speed)
        time.sleep(0.005) #0.005

except KeyboardInterrupt:
    pass
