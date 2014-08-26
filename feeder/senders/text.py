import threading
import random
from feeder.senders.base import Base

class Text(Base):
    def __init__(self, whatsapp, msg):
        self.body = msg['body']
        super(Text, self).__init__(whatsapp, msg)

    def performSend(self):
        self.interface.call("message_send", (str(self.jid), str(self.body)))
