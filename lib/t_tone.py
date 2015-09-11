import t_motion, t_sampler
import t_io as io
import setup



class Tone :

    def __init__ (self):
        # Sensor Instanciate
        self.motion = t_motion.Motion()
        # System Variable Manager Instanciate
        self.system = setup.System()
        # Sampler Instanciate
        self.sampler = t_sampler.Sampler(self.system)
        #INIT Modules
        self.motion.setup()
        io.setup()


    def update(self):
        self.motion.update()
        io.update()
        # print(io.get_bt_state())

        if io.get_bt_state() == 1 :
            self.sampler.rec_on()
        else:
            self.sampler.rec_off()

        self.sampler.update(self.motion.speed)
