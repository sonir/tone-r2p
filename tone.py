import sys, time, os
sys.path.append('/home/pi/tone/lib') # set search path
import t_tone

# Instanciate tone
tone = t_tone.Tone()

# Main Loop
print("Start main loop...")
try:
    while(1):
        tone.update()
        time.sleep(0.005) #0.005

except KeyboardInterrupt:
    pass
