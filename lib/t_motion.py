import smbus

class Motion:
    """ Motion Detection with Sensor """

    def __init__(self):
        print 'motion instanciated.'
        #Set Basic Variables
        self.pre_acc = 0 #for strage previous acc
        self.low_pass = 0.025 #0.03, 0.05
        self.diff_total = 0
        self.one_rotation = 3.14
        self.rotation = self.one_rotation * 10 #7.52

        #Variables for Speed Culcuration
        self.speed = 0
        self.speed_highpass = 0.0001
        self.speed_ave = 10 #culcurate * 0.005 sec ave
        self.speedList = [0,0]

        for var in range(0, self.speed_ave):
            self.speedList.append(0)

        #create instance of smbus
        self.bus = smbus.SMBus(1)
        #IC address
        self.address = 0x1D
        #addresses of each axis
        self.x_adr = 0x32
        self.y_adr = 0x34
        self.z_adr = 0x36

    #inicialize senser
    def init_ADXL345(self):
        self.bus.write_byte_data(self.address, 0x2D, 0x08)


    #get data from IC
    def measure_acc(self,adr):
        #read lower bytes of each axis
        self.acc0 = self.bus.read_byte_data(self.address, adr)
        #read higer bytes of each axis
        self.acc1 = self.bus.read_byte_data(self.address, adr + 1)

        #unite 2byte datas into 10byte
        self.acc = (self.acc1 << 8) + self.acc0

        #check if 10th byte is 10
        if self.acc > 0x1FF:
            #minus
            self.acc = (65536 - self.acc) * -1

        self.acc = self.acc * 3.9/1000

        return self.acc

    def setup(self):
        self.init_ADXL345()


    def update(self):
        self.x_acc = self.measure_acc(self.x_adr)
        self.y_acc = self.measure_acc(self.y_adr)
        self.z_acc = self.measure_acc(self.z_adr)

        #Culcurate Rotation
        self.acc = self.x_acc*self.y_acc*self.z_acc
        self.diff = abs(self.acc - self.pre_acc)

        if self.diff < self.low_pass:
            self.diff = 0.0

        self.diff_total += self.diff

        if self.diff_total > self.one_rotation: #rotation limitter
            self.diff_total = self.one_rotation

        self.rescaled = self.diff_total / self.one_rotation

        #Culcurate Speed
        del self.speedList[0]
        self.speedList.append(self.diff)
        for var in range(0, self.speed_ave):
            self.speed += self.speedList[var]

        self.speed /= self.speed_ave

        if self.speed < self.speed_highpass:
            self.speed = 0.0

        #check if it makes one rotation
        self.isRotate = 0
        if self.diff_total >= self.one_rotation:
            self.isRotate = 1
            self.diff_total = 0 #reset counter

        # print(self.speed)
        #print("ehehe")
        #create OSC Message
        # msg.setAddress("/acs/motion")
        # msg.append(isRotate)
        # msg.append(speed)
        # client.sendto(msg, OSCaddress)

        # #print(rescaled)

        #storage now acc as pre
        self.pre_acc = self.acc
