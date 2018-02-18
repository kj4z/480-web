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
    port='COM2',
    baudrate=9600
)

ser.isOpen()

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
	cmd = 'FB' + self.get_query_argument('f') +';'
	cmd = str(cmd)
	self.set_header('Access-Control-Allow-Origin', '*')
        self.write("SET" + cmd)
	ser.write(cmd)
	print cmd

class SetCWSpeedHandler(tornado.web.RequestHandler):
    def get(self):
	global ser
	cmd = 'KS' + self.get_query_argument('s').zfill(3) +';'
	cmd = str(cmd)
	self.set_header('Access-Control-Allow-Origin', '*')
        self.write("SPD " + cmd)
	ser.write(cmd)
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

class ToggleHandler(tornado.web.RequestHandler):
    def get(self):
	global vfo
	global ser
	self.set_header('Access-Control-Allow-Origin', '*')
	if (vfo == 0):
		self.write("TXB")
		ser.write('FR0;')
		ser.write('FT1;')
		ser.write('FW0200;') # set filter bandwidth to 200 Hz
		vfo = 1
	else:
		self.write("TXA")
		ser.write('FR1;')
		ser.write('FT0;')
		ser.write('FW2000;') # set filter bandwidth to 2 kHz
		vfo = 0

def make_app():
    return tornado.web.Application([
        (r"/u", UpHandler),
	(r"/d", DownHandler),
	(r"/v", ToggleHandler),
	(r"/f", FreqHandler),
	(r"/s", SetFreqHandler),
	(r"/c", SetCWSpeedHandler),
	(r"/k", SendCWHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(7388)
    tornado.ioloop.IOLoop.current().start()




#ser.write('PS;')

#time.sleep(1)

#while ser.inWaiting() > 0:
#	sys.stdout.write(ser.read(1))
#	#print ser.readline()
