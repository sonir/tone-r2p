import sys, time, os
sys.path.append('/home/pi/tone/lib') # set search path



import t_osc

osc = t_osc.Osc('224.0.0.1',5678)
osc.send("foo",2)
osc.send("foo2",2)
