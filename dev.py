import sys, time, os
sys.path.append('/home/pi/tone/lib') # set search path

import t_sampler, setup


# System Variable Manager Instanciate
system = setup.System()
# Sampler Instanciate
sampler = t_sampler.Sampler(system)

sampler.rec(False)
sampler.rec(True)
