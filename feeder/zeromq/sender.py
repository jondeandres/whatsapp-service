import zmq

class Sender:
    def __init__(self, whatsapp):
        self.context = whatsapp.context
        self.socket = self.context.socket(zmq.REQ)

    def connect(self):
        self.socket.connect('tcp://127.0.0.1:5555')

    def send(self, msg):
        self.socket.send(msg)
        self.socket.recv()
