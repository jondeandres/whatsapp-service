import zmq

class Sender:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect('tcp://127.0.0.1:5555')
        self.send('Connected!')


    def deliver(self, node):
        print(node)

    def send(self, msg):
        self.socket.send(msg)
        self.socket.recv()
