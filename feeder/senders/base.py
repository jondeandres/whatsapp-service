import threading
import random

class Base(object):
    def __init__(self, whatsapp, msg):
        self.jid = msg['jid']
        self.whatsapp = whatsapp
        self.interface = whatsapp.methodsInterface
        self.timer = None

    def prepare(self):
        pass

    def prepareToSend(self):
        self.interface.call("presence_sendAvailable",)
        self.whatsapp.contacts.addContact(self.jid)
        self.interface.call("typing_send",(self.jid,))
        self.interface.call("typing_paused",(self.jid,))

    def send(self):
        self.prepareToSend()
        self.performSend()
        self.setUnavailableTimer()

    def performSend(self):
        pass

    def setUnavailable(self):
        print('Executing timer method')
        self.interface.call("presence_sendUnavailable",)
        self.timer = None

    def setUnavailableTimer(self):
        if self.timer is not None: return

        wait_time = random.randrange(10, 40)
        self.timer = threading.Timer(wait_time, self.setUnavailable)
        self.timer.start()
