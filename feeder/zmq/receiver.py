import zmq
import threading
import json
import random
from feeder.senders import text
from feeder.senders import url_image

class Receiver:
    def __init__(self, whatsapp):
        self.whatsapp = whatsapp
        self.interface = whatsapp.methodsInterface
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
            self.dispatch_message(msg)

    def dispatch_message(self, msg):
        klass = None

        if msg['type'] == 'text':
            klass = text.Text
        elif msg['type'] == 'url_image':
            klass = url_image.UrlImage

        sender = klass(self.whatsapp, msg)
        sender.prepare()
        sender.send()

