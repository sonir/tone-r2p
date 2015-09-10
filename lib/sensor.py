#defines
#mode = "GLOBAL"
mode = "LOCAL"

#import libraries
import smbus
import time
import OSC
import RPi.GPIO as GPIO

#Define Sysrtem Variables
port = 5678
if mode == 'GLOBAL':
    ip_adr = '224.0.0.1'
else:
    ip_adr = '127.0.0.1'

pre_acc = 0 #for strage previous acc
#low_pass = 0.015
low_pass = 0.03 #0.05
diff_total = 0
one_rotation = 3.14
rotation = one_rotation * 10 #7.52

#Speed Culcuration Settings
speed = 0
speed_highpass = 0.0001
speed_ave = 10 #culcurate * 0.005 sec ave
speedList = [0,0]
for var in range(0, speed_ave):
    speedList.append(0)


#Setup GPIOS
GPIO.setmode(GPIO.BOARD)
SW = 7
GPIO.setup(SW, GPIO.IN)

REC_LED = 11
GPIO.setup(REC_LED, GPIO.OUT, initial = GPIO.HIGH)
PLAY_LED = 13
GPIO.setup(PLAY_LED, GPIO.OUT, initial = GPIO.HIGH)

#create instance of smbus
bus = smbus.SMBus(1)

#IC address
address = 0x1D

#addresses of each axis
x_adr = 0x32
y_adr = 0x34
z_adr = 0x36

#inicialize senser
def init_ADXL345():
    bus.write_byte_data(address, 0x2D, 0x08)


#get data from IC
def measure_acc(adr):
    #read lower bytes of each axis
    acc0 = bus.read_byte_data(address, adr)
    #read higer bytes of each axis
    acc1 = bus.read_byte_data(address, adr + 1)

    #unite 2byte datas into 10byte
    acc = (acc1 << 8) + acc0

    #check if 10th byte is 10
    if acc > 0x1FF:
        #minus
        acc = (65536 - acc) * -1

    acc = acc * 3.9/1000

    return acc


client = OSC.OSCClient()
OSCaddress = (ip_adr, port)

init_ADXL345()

try:
    while(1):
        SW_in = GPIO.input(SW)
        msg = OSC.OSCMessage()

        if SW_in == 1:
            msg.setAddress("/rec_sw")
            msg.append(1)

            client.sendto(msg, OSCaddress)

            #Wait until switch released
            counter = 0
            while GPIO.input(SW) == 1:
                if counter < 50:
                    GPIO.output(REC_LED, GPIO.HIGH)
                    GPIO.output(PLAY_LED, GPIO.HIGH)
                else:
                    GPIO.output(REC_LED, GPIO.LOW)
                    GPIO.output(PLAY_LED, GPIO.LOW)
                counter += 1;
                if counter > 100:
                    counter = 0

                time.sleep(0.01)

            msg = OSC.OSCMessage()
            msg.setAddress("/rec_sw")
            msg.append(0)
            client.sendto(msg, OSCaddress)

            GPIO.output(REC_LED, GPIO.LOW)
            GPIO.output(PLAY_LED, GPIO.LOW)

        else:
            x_acc = measure_acc(x_adr)
            y_acc = measure_acc(y_adr)
            z_acc = measure_acc(z_adr)

            #Culcurate Rotation
            acc = x_acc*y_acc*z_acc
            diff = abs(acc - pre_acc)

            if diff < low_pass:
                diff = 0

            diff_total += diff

            if diff_total > one_rotation: #rotation limitter
                diff_total = one_rotation

            rescaled = diff_total / one_rotation

            #Culcurate Speed
            del speedList[0]
            speedList.append(diff)
            for var in range(0, speed_ave):
                speed += speedList[var]

            speed /= speed_ave

            if speed < speed_highpass:
                speed = 0.0

            #check if it makes one rotation
            isRotate = 0
            if diff_total >= one_rotation:
                isRotate = 1
                diff_total = 0 #reset counter

            #create OSC Message
            msg.setAddress("/acs/motion")
            msg.append(isRotate)
            msg.append(speed)
            client.sendto(msg, OSCaddress)
            #print(rescaled)

            #storage now acc as pre
            pre_acc = acc

            time.sleep(0.005) #0.005


except KeyboardInterrupt:
    pass
