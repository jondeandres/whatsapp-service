import zmq
import threading
import json

class Receiver:
    def __init__(self, whatsapp):
        self.whatsapp = whatsapp
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)

        self.thread = None

    def bind(self):
        self.socket.bind('tcp://*:5556')
        self.spawn_thread()

    def spawn_thread(self):
        self.thread = threading.Thread(target=self.recv)
        self.thread.start()
        self.thread.join

    def recv(self):
        while True:
            msg = json.loads(self.socket.recv())
            self.socket.send('received!')
            self.whatsapp.call("message_send", (str(msg['jid']), str(msg['body'])))
