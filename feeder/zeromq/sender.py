import zmq
import ConfigParser

class Sender:
    def __init__(self, whatsapp):
        self.context = whatsapp.context
        self.socket = self.context.socket(zmq.REQ)
        self.config = ConfigParser.ConfigParser()
        self.config.read("../feeder.cfg")

    def connect(self):
        self.socket.connect(self.config.get('zeromq','protocol') + '://' + self.config.get('zeromq','sender_host') + ':' + self.config.get('zeromq','sender_port'))

    def send(self, msg):
        self.socket.send(msg)
        self.socket.recv()
