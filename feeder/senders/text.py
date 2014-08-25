import threading
import random

class Text:
    def __init__(self, whatsapp, msg):
        self.jid = msg['jid']
        self.body = msg['body']
        self.whatsapp = whatsapp
        self.interface = whatsapp.methodsInterface
        self.timer = None

    def prepare(self):
        pass

    def send(self):
        self.interface.call("presence_sendAvailable",)
        self.whatsapp.contacts.addContact(self.jid)
        self.interface.call("typing_send",(self.jid,))
        self.interface.call("typing_paused",(self.jid,))
        self.interface.call("message_send", (str(self.jid), str(self.body)))

        self.setUnavailableTimer()

    def setUnavailable(self):
        print('Executing timer method')
        self.interface.call("presence_sendUnavailable",)
        self.timer = None

    def setUnavailableTimer(self):
        if self.timer is not None: return

        wait_time = random.randrange(10, 40)
        self.timer = threading.Timer(wait_time, self.setUnavailable)
        self.timer.start()
