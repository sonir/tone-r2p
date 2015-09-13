import t_motion, t_sampler, t_metro
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
        #Instanciate Timer Named metro
        self.metro = t_metro.Metro(0.2)
        #INIT Modules
        self.motion.setup()
        io.setup()


    def update(self):
        self.motion.update()
        if self.motion.isRotate == 1 :
                self.sampler.count_round()

        io.update()

        if io.get_bt_state() == 1 :
            self.sampler.rec_on()
        else:
            self.sampler.rec_off()

        self.sampler.update(self.motion.speed)

        if self.metro.update():
            if self.sampler.rec_state :
                io.blink()
            else:
                io.led_on()
