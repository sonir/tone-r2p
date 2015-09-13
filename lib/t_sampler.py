import t_osc

class Sampler:

    def __init__(self, system):
        # OSC Instanciate
        self.osc = t_osc.Osc(system.send_ip, system.PORT)
        #State Processing
        self.rec_state = False
        self.osc.send("/s/test" , 1)
        # Set Spd Rance
        self.SEG1 = 0.003 #x0
        self.SEG2 = 0.004 #x0.2
        self.SEG3 = 0.005 #x0.5
        self.SEG4 = 0.02 #x0.66(AVG.L)
        self.SEG5 = 0.10#x1(AVG_H)  0.015
        self.SEG6 = 0.4 #x1.5
        self.SEG7 = 0.8 #x2
        self.SEG8 = 1.5 #x2.6 more:x5
        self.SP1 = 0.0
        self.SP2 = 0.2
        self.SP3 = 0.5
        self.SP4 = 0.66
        self.SP5 = 1.0
        self.SP6 = 1.5
        self.SP7 = 2.0
        self.SP8 = 2.6
        self.SP9 = 5.0
        self.sp = 0.0

        # ORG
        # self.SEG1 = 0.003
        # self.SEG2 = 0.004
        # self.SEG3 = 0.005
        # self.SEG4 = 0.002 #AVG_LOW
        # self.SEG5 = 0.15 #AVG_HIGH
        # self.SEG6 = 0.4
        # self.SEG7 = 0.8
        # self.SEG8 = 1.5
        # self.SP1 = 0.0
        # self.SP2 = 0.2
        # self.SP3 = 0.5
        # self.SP4 = 0.66
        # self.SP5 = 1.0
        # self.SP6 = 1.5
        # self.SP7 = 2.0
        # self.SP8 = 2.6
        # self.SP9 = 5.0


    def rec_on(self):
        if self.rec_state == False :
            self.rec_state = True
            self.osc.send("/s/rec/st" , 1)

    def rec_off(self):
        if self.rec_state == True :
            self.rec_state = False
            self.osc.send("/s/rec/ed" , 1)

    def vari_play(self):
        self.osc.send("/s/play/vp",1)

    def play(self):
        self.osc.send("/s/play/st",1)

    def stop(self):
        self.osc.send("/s/play/ed",1)

    def pause(self):
        self.osc.send("/s/play/ps",1)

    def update_spd(self, val):
        if self.SEG1 >= val :
            self.sp = self.SP1
            #print("SEG1" , val)
        elif self.SEG2 >= val :
            self.sp = self.SP2
            #print("SEG2" , val)
        elif self.SEG3 >= val :
            self.sp = self.SP3
            #print("SEG3" , val)
        elif self.SEG4 >= val :
            self.sp = self.SP4
            #print("SEG4" , val)
        elif self.SEG5 >= val :
            self.sp = self.SP5
            #print("SEG5" , val)
        elif self.SEG6 >= val :
            self.sp = self.SP6
            #print("SEG6" , val)
        elif self.SEG7 >= val :
            self.sp = self.SP7
            #print("SEG7" , val)
        elif self.SEG8 >= val :
            self.sp = self.SP8
            #print("SEG8" , val)
        elif self.SEG8 < val :
            self.sp = self.SP9
            #print("SEG9" , val)

        self.osc.send("/s/scratch",self.sp)

    def update(self, spd2):
        if self.rec_state != True :
            if spd2 > 0 :
                self.update_spd(spd2)
                self.vari_play()
            else :
                # self.stop()
                pass


    def count_round (self):
        self.osc.send("/round/count" , 1)
