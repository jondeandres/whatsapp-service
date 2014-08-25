import zmq
import threading
import json
import random

class Receiver:
    def __init__(self, whatsapp):
        self.whatsapp = whatsapp
        self.interface = whatsapp.methodsInterface
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)

        self.thread = None
        self.timer = None

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
            self.send_message(msg)

    def send_message(self, msg):
        jid = msg['jid']

        self.interface.call("presence_sendAvailable",)
        self.whatsapp.contacts.addContact(jid)
        self.interface.call("typing_send",(jid,))
        self.interface.call("typing_paused",(jid,))
        self.interface.call("message_send", (str(jid), str(msg['body'])))

        self.setUnavailableTimer()

    def setUnavailable(self):
        print('Executing timer method')
        self.interface.call("presence_sendUnavailable",)
        self.timer = None

    def setUnavailableTimer(self):
        if self.Timer is not None: return

        wait_time = random.randrange(10, 40)
        self.timer = threading.Timer(wait_time, self.setUnavailable)
        self.timer.start()
