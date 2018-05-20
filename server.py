import time
import serial
import sys
import tornado.ioloop
import tornado.web
from tornado.log import enable_pretty_logging


enable_pretty_logging()


is_closing = False

vfo = 0


# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    #port='COM2',
    port='/dev/ttyUSB0',
    baudrate=9600
)

ser.isOpen()


class SetSimplexUSB(tornado.web.RequestHandler):
    def get(self):
        global vfo
        global ser
        self.set_header('Access-Control-Allow-Origin', '*')
        ser.write('MD2;')
        ser.write('FR0;')
        ser.write('FT0;')

class BandUp(tornado.web.RequestHandler):
    def get(self):
        global ser
        ser.write('BU;')
        self.set_header('Access-Control-Allow-Origin', '*')

class BandDown(tornado.web.RequestHandler):
    def get(self):
        global ser
        ser.write('BD;')
        self.set_header('Access-Control-Allow-Origin', '*')

class CloneVFO(tornado.web.RequestHandler):
    def get(self):
        global ser
        ser.write('VV;')
        self.set_header('Access-Control-Allow-Origin', '*')

class UpHandler(tornado.web.RequestHandler):
    def get(self):
        global ser
        self.write("UP")
        ser.write('CH0;')

class DownHandler(tornado.web.RequestHandler):
    def get(self):
        global ser
        self.write("DOWN")
        ser.write('CH1;')

class SetFreqHandler(tornado.web.RequestHandler):
    def get(self):
        global ser
        freqa = ''
        freqb = ''
        try:
                freqa = self.get_query_argument('fa')
        except tornado.web.MissingArgumentError:
                pass
        try:
                freqb = self.get_query_argument('fb')
        except tornado.web.MissingArgumentError:
                pass
        if freqa:
                cmd = 'FA' + freqa +';'
        elif freqb:
                cmd = 'FB' + freqb +';'
        else:
                return
        cmd = str(cmd)
        self.set_header('Access-Control-Allow-Origin', '*')
        self.write("SET" + cmd)
        ser.write(cmd)
        print cmd

class SetCWSpeedHandler(tornado.web.RequestHandler):
    def get(self):
        global ser
        speed = self.get_query_argument('s').zfill(3)
        if speed == 'TBD':
            speed = ''
        cmd = str('KS' + speed + ';')
        self.set_header('Access-Control-Allow-Origin', '*')
        ser.write(cmd)
        if speed == '':
            speed = ser.read(6)[3:5]
        self.write("SPD " + speed)
        print cmd

class SendCWHandler(tornado.web.RequestHandler):
    def get(self):
        global ser
        cmd = 'KY ' + self.get_query_argument('s').ljust(24) +';' #padded out to 24 chars
        cmd = str(cmd)
        self.set_header('Access-Control-Allow-Origin', '*')
        self.write("KY " + cmd)
        ser.write(cmd)
        print cmd

class PowerOn(tornado.web.RequestHandler):
    def get(self):
        global ser
        # set power status on, spam it to wake up
        ser.write(';;;;PS1;')
        ser.write(';;;;PS1;')
        time.sleep(1)
        ser.write(';;;;PS1;')
        self.set_header('Access-Control-Allow-Origin', '*')
        time.sleep(1)
        time.sleep(1)

class PowerOff(tornado.web.RequestHandler):
    def get(self):
        global ser
        ser.write(';;;;PS0;')

class FreqHandler(tornado.web.RequestHandler):
    def get(self):
        global ser

        ser.write('FA;FB;')
        time.sleep(1)
        freq = ''
        while ser.inWaiting() > 0:
                freq += ser.read(1)

        parts = freq.split('FA')
        freq_a = parts[1]
        parts = freq_a.split(';')
        freq_a = parts[0]
        
        parts = freq.split('FB')
        freq_b = parts[1]
        parts = freq_b.split(';')
        freq_b = parts[0]

        self.set_header('Access-Control-Allow-Origin', '*')
        self.write(freq_a + ';' + freq_b)

class SetAudioGain(tornado.web.RequestHandler):
    def get(self):
        global ser
        self.set_header('Access-Control-Allow-Origin', '*')
        cmd = "AG0" + self.get_query_argument('g').zfill(3) + ";"
        ser.write(cmd)

class ToggleHandler(tornado.web.RequestHandler):
    def get(self):
        global vfo
        global ser
        self.set_header('Access-Control-Allow-Origin', '*')
        a = "FW" + self.get_query_argument('a').zfill(4) + ";"
        b = "FW" + self.get_query_argument('b').zfill(4) + ";"
        if (vfo == 0):
                self.write("TXB")
                ser.write(b) # set filter bandwidth to Bfilter
                ser.write('FR0;')
                ser.write('FT1;')
                ser.write(a) # set filter bandwidth to Afilter
                vfo = 1
        else:
                self.write("TXA")
                ser.write(a) # set filter bandwidth to Afilter
                ser.write('FR1;')
                ser.write('FT0;')
                ser.write(b) # set filter bandwidth to Bfilter
                vfo = 0

class SetCW(tornado.web.RequestHandler):
    def get(self):
        global vfo
        global ser
        self.set_header('Access-Control-Allow-Origin', '*')
        if (vfo == 0):
            ser.write('MD7;')
            ser.write('FR1;')
            ser.write('FT0;')
            time.sleep(1)
            ser.write('MD3;')
            ser.write('FR0;')
            ser.write('FT1;')
        else:
            ser.write('MD3;')
            ser.write('FR0;')
            ser.write('FT1;')
            time.sleep(1)
            ser.write('MD7;')
            ser.write('FR1;')
            ser.write('FT0;')

class ToggleCWR(tornado.web.RequestHandler):
    def get(self):
        global ser
        self.set_header('Access-Control-Allow-Origin', '*')
        ser.write('MD;')
        mode = ser.read(4)[-2]
        if mode == '7':
            ser.write('MD3;')
        if mode == '3':
            ser.write('MD7;')

class ToggleVox(tornado.web.RequestHandler):
    def get(self):
        global ser
        self.set_header('Access-Control-Allow-Origin', '*')
        vox = ''
        ser.write('VX;')
        vox = ser.read(4)
        voxstat = vox[2]
        if (voxstat == '1'):
            vox='0'
        else:
            vox='1'
	self.write(vox)
        cmd = 'VX' + vox +';'
        ser.write(cmd)

class Tune(tornado.web.RequestHandler):
    def get(self):
        global ser
        meter = ''
        ser.write('TX2;')
        ser.write('RM;')
        time.sleep(2)
        meter = ser.read(24)
        ser.write('RX;')
        dec = int(meter.split(';')[0][-2:])
        if (dec <= 1):
            swr = '1.1'
        if (dec == 2):
            swr = '1.3'
        if (dec == 3):
            swr = '1.6'
        if (dec == 4):
            swr = '1.9'
        if (dec == 5):
            swr = '2.3'
        if (dec == 6):
            swr = '3'
        if (dec > 6):
            swr = '>3'
        self.set_header('Access-Control-Allow-Origin', '*')
        self.write(swr)


def make_app():
    return tornado.web.Application([
        (r"/u", UpHandler),
        (r"/d", DownHandler),
        (r"/v", ToggleHandler),
        (r"/f", FreqHandler),
        (r"/s", SetFreqHandler),
        (r"/c", SetCWSpeedHandler),
        (r"/k", SendCWHandler),
        (r"/x", ToggleVox),
        (r"/t", Tune),
        (r"/r", ToggleCWR),
        (r"/ps1", PowerOn),
        (r"/ps0", PowerOff),
        (r"/bu", BandUp),
        (r"/bd", BandDown),
        (r"/vv", CloneVFO),
        (r"/cw", SetCW),
        (r"/usb", SetSimplexUSB),
        (r"/ag", SetAudioGain),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(7388)
    tornado.ioloop.IOLoop.current().start()




#ser.write('PS;')

#time.sleep(1)

#while ser.inWaiting() > 0:
#        sys.stdout.write(ser.read(1))
#        #print ser.readline()
