class System:
    '''System Variables of System'''

    def __init__ (self):
        #send mode
        self.MODE = 'GLOBAL'
        #self.mode = 'LOCAL'

        self.PORT = 57110

        if self.MODE == 'GLOBAL':
            print("MODE: GLOBAL")
            self.send_ip = '224.0.0.1'
        else:
            print("MODE: LOCAL")
            self.send_ip = '127.0.0.1'
